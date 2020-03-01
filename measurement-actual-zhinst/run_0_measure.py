import library_path
dir_measurement = library_path.find_append_path()

import config_measurement
import program

def run():
  dict_config_setup = config_measurement.get_dict_config_setup()
  print(dict_config_setup)
  configSetup = program.get_configSetup_by_filename(dict_config_setup)
  dir_raw = program.measure(configSetup, dir_measurement)

  program.run_condense_dir_raw(dir_raw=dir_raw, do_plot=False)

if __name__ == '__main__':
  run()