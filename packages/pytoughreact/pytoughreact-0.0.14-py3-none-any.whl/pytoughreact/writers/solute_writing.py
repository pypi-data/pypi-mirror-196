'''
MIT License

Copyright (c) [2022] [Temitope Ajayi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import os
import sys
from fixed_format_file import default_read_function, fixed_format_file
from t2data import t2data
from constants.format_specifications import t2solute_format_specification
from constants.sections import t2solute_sections
from constants.defaults_constants import DEFAULT_OPTIONS, DEFAULT_CONSTRAINTS, DEFAULT_READIO, DEFAULT_WEIGHT_DIFFUSION, DEFAULT_TOLERANCE, DEFAULT_PRINTOUT, DEFAULT_ZONE
from exceptions.custom_error import ReactiveOptionsError, RequiredInputException, ReactiveConstraintsError
from copy import deepcopy

class t2solute_parser(fixed_format_file):
    """Class for parsing SOLUTE.INP data file."""

    def __init__(self, filename, mode, read_function=default_read_function):
        super(t2solute_parser, self).__init__(filename, mode,
                                              t2solute_format_specification, read_function)

    
class t2solute(t2data):
    def __init__(self, filename = '', meshfilename = '', t2chemical=None, read_function=default_read_function):
        self.t2chemical = t2chemical
        self._sections = []
        if self.t2chemical is not None:
            self.title = self.t2chemical.title
        else:
            self.title = ''
        self.options = deepcopy(DEFAULT_OPTIONS)
        self.constraints = deepcopy(DEFAULT_CONSTRAINTS)
        self.readio = deepcopy(DEFAULT_READIO)
        self.weight_diffusion = deepcopy(DEFAULT_WEIGHT_DIFFUSION)
        self.tolerance = deepcopy(DEFAULT_TOLERANCE)
        self.printout = deepcopy(DEFAULT_PRINTOUT)
        self.nodes_to_write = [-1]
        if self.t2chemical is not None:
            self.primary_species = self.t2chemical.primary_aqueous
        else:
            self.primary_species = []
        if self.t2chemical is not None:
            self.minerals = self.t2chemical.minerals
        else:
            self.minerals = []
        self.aqueous_species = [-1]
        self.adsorption_species = [-1]
        self.exchange_species = [-1]
        self.chemical_zones = deepcopy(DEFAULT_ZONE)
        self.end_keyword = '# this "end" record is needed ' \
                           '\nend\n*************************************************************************** '
        self.initial_water_index = self.t2chemical.initial_water_index
        self.boundary_water_index = self.t2chemical.boundary_water_index
        self.mineral_index = self.t2chemical.mineral_index
        self.initial_gas_index = self.t2chemical.initial_gas_index
        self.injection_gas_index = self.t2chemical.injection_gas_index
        self.perm_poro_index = self.t2chemical.perm_poro_index
        self.read_function = read_function
        self.chemical_zones_to_nodes = self.getgrid_info()
        super().__init__(filename, meshfilename, read_function)

    def getZoneValue(self, dict_to_check, value):
        key_list = list(dict_to_check.keys())
        val_list = list(dict_to_check.values())
        position = key_list.index(value)
        zone_number = val_list[position]
        return zone_number

    def getgrid_info(self):
        output = []
        viewer = []
        try:
            for block in self.t2chemical.t2grid.blocklist:
                initial_water = block.zone.water[0][0]
                mineral_in_block = block.zone.mineral_zone
                perm_poro = block.zone.permporo
                try:
                    initial_gas = block.zone.gas[0][0]
                except IndexError:
                    initial_gas = 0
                try:
                    boundary_water = block.zone.water[1][0]
                except IndexError:
                    boundary_water = 0
                try:
                    injection_gas = block.zone.gas[1][0]
                except IndexError:
                    injection_gas = 0
                initial_water_zone = self.getZoneValue(self.initial_water_index, initial_water)
                mineral_zone = self.getZoneValue(self.mineral_index, mineral_in_block)
                perm_poro_zone = self.getZoneValue(self.perm_poro_index, perm_poro)
                try:
                    initial_gas_zone = self.getZoneValue(self.initial_gas_index, initial_gas)
                    boundary_water_zone = self.getZoneValue(self.boundary_water_index, boundary_water)
                    injection_gas_zone = self.getZoneValue(self.injection_gas_index, injection_gas)
                except ValueError:
                    boundary_water_zone = 1
                    injection_gas_zone = 1
                    initial_gas_zone = 1
                appender = [block.name, 0, 0, initial_water_zone, boundary_water_zone, mineral_zone, initial_gas_zone, 0, 0,
                            perm_poro_zone, 0, injection_gas_zone]
                output.append(appender)
                viewer.append(block)
            return output
        except:
            return output

    # chemical_zones_to_nodes = property(getgrid_info)

    def update_read_write_functions(self):
        """Updates functions for reading and writing sections of data file."""

        self.read_fn = dict(zip(
            t2solute_sections,
            [self.read_title,
             self.read_options,
             self.read_constraints,
             self.read_readio,
             self.read_weight_diffu,
             self.read_tolerance,
             self.read_printout,
             self.read_nodes,
             self.read_primary_species,
             self.read_minerals,
             self.read_aqueous_species,
             self.read_adsorption_species,
             self.read_exchange_species,
             self.read_chemical_zones,
             self.read_chemical_zones_to_nodes
             ]))

        self.write_fn = dict(zip(
            t2solute_sections,
            [self.write_title,
             self.write_options,
             self.write_constraints,
             self.write_readio,
             self.write_weight_diffu,
             self.write_tolerance,
             self.write_printout,
             self.write_nodes,
             self.write_primary_species,
             self.write_minerals,
             self.write_aqueous_species,
             self.write_adsorption_species,
             self.write_exchange_species,
             self.write_chemical_zones,
             self.write_chemical_zones_to_nodes]))

    def get_present_sections(self):
        """Returns a list of TOUGH2 section keywords for which there are
        corresponding data in the t2bio object."""
        data_present = dict(zip(
            t2solute_sections,
            [self.title,
             self.options,
             self.constraints,
             self.readio,
             self.weight_diffusion,
             self.tolerance,
             self.printout,
             self.nodes_to_write,
             self.primary_species,
             self.minerals,
             self.aqueous_species,
             self.adsorption_species,
             self.exchange_species,
             self.chemical_zones,
             self.chemical_zones_to_nodes]))
        return [keyword for keyword in t2solute_sections if data_present[keyword]]

    present_sections = property(get_present_sections)

    def getGridBlocks(self):
        blk = []
        for t2block in self.t2chemical.t2grid.blocklist:
            blk.append(t2block.name)
        return blk

    def getInitialWaterIndex(self):
        water_dict = self.t2chemical.initial_water_index
        key_list = list(water_dict.keys())
        val_list = list(water_dict.values())
        return key_list, val_list

    def getInitialWater(self):
        zone_water = []
        for blk in self.t2chemical.t2grid.blocklist:
            zone_water.append(blk.zone.water[0])
        return zone_water

    def getBoundaryWaterIndex(self):
        water_dict = self.t2chemical.boundary_water_index
        key_list = list(water_dict.keys())
        val_list = list(water_dict.values())
        return key_list, val_list

    def getBoundaryWater(self):
        zone_water = []
        for blk in self.t2chemical.t2grid.blocklist:
            zone_water.append(blk.zone.water[1])
        return zone_water

    def getMineral(self):
        mineral_zone = []
        for blk in self.t2chemical.t2grid.blocklist:
            mineral_zone.append(blk.zone.mineral)
        return mineral_zone

    def section_insertion_index(self, section):
        """Determines an appropriate position to insert the specified section
        in the internal list of data file sections.
        """
        try:
            listindex = t2solute_sections.index(section)
            if listindex == 0:
                return 0  # SIMUL section
            else:
                # first look for sections above the one specified,
                # and put new one just after the last found:
                for i in reversed(range(listindex)):
                    try:
                        section_index = self._sections.index(t2solute_sections[i])
                        return section_index + 1
                    except ValueError:
                        pass
                # look for sections below the one specified,
                # and put new one just before the first found:
                for i in range(listindex, len(t2solute_sections)):
                    try:
                        section_index = self._sections.index(t2solute_sections[i])
                        return section_index
                    except ValueError:
                        pass
                return len(self._sections)
        except ValueError:
            return len(self._sections)

    def convert_to_t2solute(self, keyword):
        if 'options' in keyword.lower() and 'reactive' in keyword.lower():
            return 'OPTIONS'
        elif 'constraints' in keyword.lower() and 'reactive' in keyword.lower():
            return 'CONSTRAINTS'
        elif 'weighting' in keyword.lower() and 'diffusion' in keyword.lower():
            return 'WEIGHT_DIFFU'
        elif 'read' in keyword.lower() and 'input' in keyword.lower():
            return 'READIO'
        elif 'convergence' in keyword.lower() and 'tolerance' in keyword.lower():
            return 'TOLERANCE'
        elif 'printout' in keyword.lower() and 'control' in keyword.lower():
            return 'PRINTOUT'
        elif 'nodes' in keyword.lower() and 'output' in keyword.lower():
            return 'NODES'
        elif 'primary' in keyword.lower() and 'aqueous' in keyword.lower():
            return 'PRIMARY_SPECIES'
        elif 'mineral' in keyword.lower() and 'output' in keyword.lower():
            return 'MINERALS'
        elif 'aqueous' in keyword.lower() and 'output' in keyword.lower():
            return 'AQUEOUS_SPECIES'
        elif 'adsorption' in keyword.lower() and 'output' in keyword.lower():
            return 'ADSORPTION_SPECIES'
        elif 'exchange' in keyword.lower() and 'output' in keyword.lower():
            return 'EXCHANGE_SPECIES'
        elif 'chemical' in keyword.lower() and 'default' in keyword.lower():
            return 'CHEMICAL_ZONES'
        elif 'chemical' in keyword.lower() and 'zones' in keyword.lower():
            return 'CHEMICAL_ZONES_TO_NODES'
        else:
            return 'false'

    def write_title(self, outfile):
        if self.t2chemical is not None:
            self.title = self.t2chemical.title
        outfile.write('#Title' + '\n')
        outfile.write(self.title.strip() + '\n')

    def read_options(self, infile):
        """Reads reaction options"""
        params = infile.get_reactive_options()
        if len(params) == 0:
            raise ReactiveOptionsError
        else:
            self.__dict__['options']['iterative_scheme'] = int(params[0])
            self.__dict__['options']['rsa_newton_raphson'] = int(params[1])
            self.__dict__['options']['linear_equation_solver'] = int(params[2])
            self.__dict__['options']['activity_coefficient_calculation'] = int(params[3])
            self.__dict__['options']['gaseous_species_in_transport'] = int(params[4])
            self.__dict__['options']['result_printout'] = int(params[5])
            self.__dict__['options']['poro_perm'] = int(params[6])
            self.__dict__['options']['co2_h2o_effects'] = int(params[7])
            self.__dict__['options']['itds_react'] = int(params[8])

    def write_options(self, outfile):
        outfile.write('#options for reactive chemical transport ' + '\n')
        outfile.write('# ISPIA itersfa ISOLVC NGAMM NGAS1 ichdump kcpl Ico2h2o  nu' + '\n')
        vals = [self.options['iteration_scheme'], self.options['rsa_newton_raphson'],
                self.options['linear_equation_solver'], self.options['activity_coefficient_calculation'],
                self.options['gaseous_species_in_transport'], self.options['result_printout'],
                self.options['poro_perm'], self.options['co2_h2o_effects'],
                self.options['itds_react']]
        outfile.write_values(vals, 'options')

    def read_constraints(self, infile):
        """Reads simulation constraints"""
        params = infile.get_reactive_constraints()
        if len(params) == 0:
            raise ReactiveConstraintsError
        else:
            self.__dict__['constraints']['skip_saturation'] = float(params[0])
            self.__dict__['constraints']['courant_number'] = float(params[1])
            self.__dict__['constraints']['maximum_ionic_strength'] = float(params[2])
            self.__dict__['constraints']['weighting_factor'] = float(params[3])

    def write_constraints(self, outfile):
        outfile.write('#constraints for reactive chemical transport ' + '\n')
        outfile.write('# SL1MIN        rcour     STIMAX    CNFACT(=1 fully implicit)' + '\n')
        vals = [self.constraints['skip_saturation'], self.constraints['courant_number'],
                self.constraints['maximum_ionic_strength'], self.constraints['weighting_factor']]
        outfile.write_values(vals, 'constraints')

    def read_readio(self, infile):
        """Reads simulation title"""
        params = infile.get_readio()
        if len(params) == 0:
            raise RequiredInputException
        else:
            self.__dict__['readio']['database'] = params[0]
            self.__dict__['readio']['iteration_info'] = params[1]
            self.__dict__['readio']['aqueous_concentration'] = params[2]
            self.__dict__['readio']['minerals'] = params[3]
            self.__dict__['readio']['gas'] = params[4]
            self.__dict__['readio']['time'] = params[5]

    def write_readio(self, outfile):
        outfile.write('#Read input and output file names' + '\n')
        outfile.write(self.readio['database'] + '\n')
        outfile.write(self.readio['iteration_info'] + '\n')
        outfile.write(self.readio['aqueous_concentration'] + '\n')
        outfile.write(self.readio['minerals'] + '\n')
        outfile.write(self.readio['gas'] + '\n')
        outfile.write(self.readio['time'] + '\n')

    def read_weight_diffu(self, infile):
        """Reads weight and diffusion"""
        params = infile.get_weight_diffusion()
        if len(params) == 0:
            raise RequiredInputException
        else:
            self.__dict__['weight_diffusion']['time_weighting'] = float(params[0])
            self.__dict__['weight_diffusion']['upstream_weighting'] = float(params[1])
            self.__dict__['weight_diffusion']['aqueous_diffusion_coefficient'] = float(params[2])
            self.__dict__['weight_diffusion']['gas_diffusion_coefficient'] = float(params[3])

    def write_weight_diffu(self, outfile):
        outfile.write('# Weighting space/time, aq. and gas diffusion coeffs' + '\n')
        outfile.write('# ITIME     WUPC   DFFUN     DFFUNG' + '\n')
        vals = [self.weight_diffusion['time_weighting'], self.weight_diffusion['upstream_weighting'],
                self.weight_diffusion['aqueous_diffusion_coefficient'],
                self.weight_diffusion['gas_diffusion_coefficient']]
        outfile.write_values(vals, 'weight_diffu')

    def read_tolerance(self, infile):
        """Reads tolerance values"""
        params = infile.get_tolerance_values()
        if len(params) == 0:
            raise RequiredInputException
        else:
            self.__dict__['tolerance']['maximum_iterations_transport'] = int(params[0])
            self.__dict__['tolerance']['transport_tolerance'] = float(params[1])
            self.__dict__['tolerance']['maximum_iterations_chemistry'] = int(params[2])
            self.__dict__['tolerance']['chemistry_tolerance'] = float(params[3])
            self.__dict__['tolerance']['not_used1'] = float(params[4])
            self.__dict__['tolerance']['not_used2'] = float(params[5])
            self.__dict__['tolerance']['relative_concentration_change'] = float(params[6])
            self.__dict__['tolerance']['relative_kinetics_change'] = float(params[7])

    def write_tolerance(self, outfile):
        outfile.write('# Convergence and tolerance parameters' + '\n')
        outfile.write('#  MAXITPTR  TOLTR    MAXITPCH  TOLCH    NOT-USED  NOT-USED    TOLDC    TOLDR' + '\n')
        vals = [self.tolerance['maximum_iterations_transport'], self.tolerance['transport_tolerance'],
                self.tolerance['maximum_iterations_chemistry'], self.tolerance['chemistry_tolerance'],
                self.tolerance['not_used1'], self.tolerance['not_used2'],
                self.tolerance['relative_concentration_change'], self.tolerance['relative_kinetics_change']]
        outfile.write_values(vals, 'tolerance')

    def read_printout(self, infile):
        """Reads printout_options"""
        params = infile.get_printout_options()
        if len(params) == 0:
            raise RequiredInputException
        else:
            self.__dict__['printout']['printout_frequency'] = int(params[0])
            self.__dict__['printout']['number_of_gridblocks'] = int(params[1])
            self.__dict__['printout']['number_of_chemical_components'] = int(params[2])
            self.__dict__['printout']['number_of_minerals'] = int(params[3])
            self.__dict__['printout']['number_of_aqueous'] = int(params[4])
            self.__dict__['printout']['number_of_surface_complexes'] = int(params[5])
            self.__dict__['printout']['number_of_exchange_species'] = int(params[6])
            self.__dict__['printout']['aqueous_unit'] = int(params[7])
            self.__dict__['printout']['mineral_unit'] = int(params[8])
            self.__dict__['printout']['gas_unit'] = int(params[9])

    def write_printout(self, outfile):
        outfile.write('# Printout control variables:' + '\n')
        outfile.write('# NWTI NWNOD NWCOM NWMIN NWAQ NWADS NWEXC iconflag minflag igasflag' + '\n')
        vals = [self.printout['printout_frequency'], self.printout['number_of_gridblocks'],
                self.printout['number_of_chemical_components'], self.printout['number_of_minerals'],
                self.printout['number_of_aqueous'], self.printout['number_of_surface_complexes'],
                self.printout['number_of_exchange_species'], self.printout['aqueous_unit'],
                self.printout['mineral_unit'], self.printout['gas_unit']]
        outfile.write_values(vals, 'printout')

    def read_nodes(self, infile):
        """Reads nodes to write"""
        params = infile.get_nodes_to_read(self.t2chemical.t2grid)
        if len(params) == 0:
            pass
        else:
            self.__dict__['nodes_to_write'] = params

    def write_nodes(self, outfile):
        if self.nodes_to_write[0] == -1:
            outfile.write('# Nodes for which to output data in time file (15a5):' + '\n')
        else:
            outfile.write('# Nodes for which to output data in time file (15a5):' + '\n')
            nodes = []
            for i in range(len(self.nodes_to_write)):
                nodes.append(self.t2chemical.t2grid.blocklist[i].name)
            for node in nodes:
                outfile.write(node + '\n')

    def read_primary_species(self, infile):
        """Reads primary species to write"""
        params = infile.get_primary_species_to_read(self.t2chemical.primary_aqueous)
        if len(params) == 0:
            pass
        else:
            self.__dict__['primary_species'] = params

    def write_primary_species(self, outfile):
        outfile.write(
            '# Primary (total) aqueous species for which to output concentrations in time and plot files:' + '\n')
        if self.t2chemical is not None:
            vals = []
            for species in self.primary_species:
                vals.append(species.NAME.strip())
            for val in vals:
                outfile.write(val + '\n')
        else:
            vals = self.primary_species
            for val in vals:
                outfile.write(val + '\n')

    def read_minerals(self, infile):
        """Reads minerals to write"""
        params = infile.get_minerals_to_write(self.t2chemical.minerals)
        if len(params) == 0:
            pass
        else:
            self.__dict__['minerals'] = params

    def write_minerals(self, outfile):
        outfile.write('# Minerals for which to output data in time and plot files:' + '\n')
        if self.t2chemical is not None:
            vals = []
            for mineral in self.minerals:
                vals.append(mineral.name)
            for val in vals:
                outfile.write(val + '\n')
        else:
            vals = []
            for mineral in self.minerals:
                vals.append(mineral.name)
            for val in vals:
                outfile.write(val + '\n')

    def read_aqueous_species(self, infile):
        """Reads aqueous species to write"""
        pass

    def write_aqueous_species(self, outfile):
        # TODO find out why leaving a space doesnt run
        if self.aqueous_species[0] == -1:
            outfile.write("\n")
            # outfile.write('# Individual aqueous species for which to output concentrations in time and plot files:' + ' \n tr' )
            outfile.write(
                '# Individual aqueous species for which to output concentrations in time and plot files:' + '\n')

    def read_adsorption_species(self, infile):
        """Reads adsorption_species to write"""
        pass

    def write_adsorption_species(self, outfile):
        if self.adsorption_species[0] == -1:
            outfile.write('# Adsorption species for which to output concentrations in time and plot files:' + ' \n')

    def read_exchange_species(self, infile):
        """Reads exchange species to write"""
        pass

    def write_exchange_species(self, outfile):
        if self.exchange_species[0] == -1:
            outfile.write('# Exchange species for which to output concentrations in time and plot files:' + ' \n')

    def read_chemical_zones(self, infile):
        """Reads default chemical zones"""
        params = infile.get_default_chemical_zones()
        if len(params) == 0:
            raise RequiredInputException
        else:
            self.__dict__['chemical_zones']['IZIWDF'] = int(params[0])
            self.__dict__['chemical_zones']['IZBWDF'] = int(params[1])
            self.__dict__['chemical_zones']['IZMIDF'] = int(params[2])
            self.__dict__['chemical_zones']['IZGSDF'] = int(params[3])
            self.__dict__['chemical_zones']['IZADDF'] = int(params[4])
            self.__dict__['chemical_zones']['IZEXDF'] = int(params[5])
            self.__dict__['chemical_zones']['IZPPDF'] = int(params[6])
            self.__dict__['chemical_zones']['IZKDDF'] = int(params[7])
            self.__dict__['chemical_zones']['IZBGDF'] = int(params[8])

    def write_chemical_zones(self, outfile):
        outfile.write('# Default types of chemical zones' + '\n')
        outfile.write('# Initial  Boundary                                      Porosity/ ' + '\n')
        outfile.write(
            '#  Water    Water   Minerals   Gases Adsorption Exchange  Permeab  Kd zones  Injection Gas Zones' + '\n')
        outfile.write('# IZIWDF   IZBWDF    IZMIDF   IZGSDF   IZADDF    IZEXDF   IZPPDF    IZKDDF     IZBGDF' + '\n')
        vals = [self.chemical_zones['IZIWDF'], self.chemical_zones['IZBWDF'],
                self.chemical_zones['IZMIDF'], self.chemical_zones['IZGSDF'],
                self.chemical_zones['IZADDF'], self.chemical_zones['IZEXDF'],
                self.chemical_zones['IZPPDF'], self.chemical_zones['IZKDDF'],
                self.chemical_zones['IZBGDF']]
        outfile.write_values(vals, 'chemical_zones')

    def map_zone_to_blocks(self, params):
        for param in params:
            grid_name = param[0]
            zone = self.t2chemical.t2grid.block[grid_name].zone
            if zone.water is None:
                zone.gas = [[], []]
                zone.water = [[], []]
                # nseq = int(param[1])
                # nadd = int(param[2])
                initial_water = int(param[3])
                boundary_water = int(param[4])
                mineral = int(param[5])
                initial_gas = int(param[6])
                # adsorption = int(param[7])
                # exchange = int(param[8])
                perm_poro = int(param[9])
                # decay_zone = int(param[10])
                injection_gas = int(param[11])
                zone.mineral_zone = self.t2chemical.initial_minerals_mapping[mineral]
                zone.gas[0] = self.t2chemical.initial_gas_mapping[initial_gas]
                try:
                    zone.gas[1] = self.t2chemical.injection_gas_mapping[injection_gas]
                except:
                    pass
                zone.water[0] = self.t2chemical.initial_waters_mapping[initial_water]
                try:
                    zone.water[1] = self.t2chemical.boundary_waters_mapping[boundary_water]
                except:
                    pass
                zone.permporo = self.t2chemical.initial_perm_poro_mapping[perm_poro]
            else:
                pass

    def read_chemical_zones_to_nodes(self, infile):
        """Reads simulation title"""
        params = infile.get_default_chemical_zone_to_nodes()
        if len(params) == 0:
            block_data = self.generate_zone_to_blocks()
            self.map_zone_to_blocks(block_data)
            self.__dict__['chemical_zones_to_nodes'] = block_data
        else:
            self.map_zone_to_blocks(params)
            self.__dict__['chemical_zones_to_nodes'] = params

    def generate_zone_to_blocks(self):
        all_blocks = []
        for block in self.t2chemical.t2grid.blocklist:
            all_blocks.append([block.name, 0, 0] + list(self.chemical_zones.values()))
        return all_blocks

    def write_chemical_zones_to_nodes(self, outfile):
        outfile.write('# Types of chemical zones for specific nodes (optional)' + '\n')
        outfile.write('# Gridblock  Gridblocks Increment   Water    Water     Minerals   Gases  Adsorption Exchange  '
                      'Permeab  Kd zones Injection Gas Zones' + '\n')
        outfile.write('# ELEM(a5)   NSEQ         NADD       IZIWDF   IZBWDF    IZMIDF   IZGSDF   IZADDF    IZEXDF    '
                      'IZPPDF   IZKDDF     IZBGDF' + '\n')
        for vals in self.chemical_zones_to_nodes:
            outfile.write_values(vals, 'chemical_zones_to_nodes')

    def write(self, filename='', meshfilename='', runlocation='',
              extra_precision=None, echo_extra_precision=None):
        if runlocation:
            if not os.path.isdir(runlocation):
                os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename == '':
            filename = 'solute.inp'
        self.update_sections()
        self.update_read_write_functions()
        outfile = t2solute_parser(filename, 'w')
        for keyword in self._sections:
            self.write_fn[keyword](outfile)
            outfile.write('\n')
        outfile.write(self.end_keyword + '\n')
        self.status = 'successful'
        outfile.close()

    def read(self, filename='', meshfilename='', runlocation='', extra_precision=None, echo_extra_precision=None):
        if runlocation:
            if not os.path.isdir(runlocation):
                os.mkdir(runlocation)
            os.chdir(runlocation)
        if filename:
            self.filename = filename
        mode = 'r' if sys.version_info > (3,) else 'rU'
        infile = t2solute_parser(self.filename, mode, read_function=self.read_function)
        self.read_title(infile)
        self._sections = []
        self.update_read_write_functions()
        more = True
        next_line = None
        # countline = 0
        while more:
            if next_line:
                line = next_line
            else:
                line = infile.readline()
            if line:
                # keyword = line[0: 5].strip()
                keyword = line[1:]
                check_presence = self.convert_to_t2solute(keyword)
                if keyword in ['ENDCY', 'ENDFI', 'end']:
                    more = False
                    self.end_keyword = keyword
                # elif keyword in t2chemical_read_sections:
                # elif any(ext in keyword for ext in t2chemical_read_sections):
                elif check_presence != 'false':
                    keyword = check_presence
                    fn = self.read_fn[keyword]
                    next_line = None
                    if keyword == 'SHORT':
                        fn(infile, line)
                    elif keyword == 'PARAM':
                        next_line = fn(infile)
                    else:
                        fn(infile)
                    self._sections.append(keyword)
            else:
                more = False
        self.status = 'successful'
        infile.close()
