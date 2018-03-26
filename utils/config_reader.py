#!usr/bin/env python
# coding: utf-8

# author: haidong zhang
# date: 2017.04.01
# function: this class is used to read configuration information from config files.

import ConfigParser


class ConfigReader(object):
    def __init__(self, config_filename):
        '''
        返回配置文件名称
        ---------------------------------------------------------------
         Parameters:
             config_filename: str
                配置文件名称
        '''
        self.config_parser = ConfigParser.ConfigParser()
        self.config_parser.read(config_filename)

    def __getitem__(self, key):
        '''
        返回配置文件里面的值
         -------------------------------------------------------------
         Parameters:
             key: tuple, or list(). len(key) = 3
                key[0]: section
                key[1]: sub_section
                key[2]: 返回值类型，包括string/int/float/bool
                examples: key = ('path', 'filename', 'string')表示取path的filename的值，类型为string
        Return:
            根据type，返回string, int, float, 或bool
        '''
        assert(len(key) == 3)
        try:
            if key[2] == 'string':
                return self.get_parameter_string(key[0], key[1])
            elif key[2] == 'bool':
                return self.get_parameter_bool(key[0], key[1])
            elif key[2] == 'int':
                return self.get_parameter_int(key[0], key[1])
            elif key[2] == 'float':
                return self.get_parameter_float(key[0], key[1])
        except:
            print 'Error, please check the keys.'
            raise KeyError

    def get_parameter_string(self, section, key):
        return self.config_parser.get(section, key)

    def get_parameter_int(self, section, key):
        return int(self.get_parameter_string(section, key))

    def get_parameter_float(self, section, key):
        return float(self.get_parameter_string(section, key))

    def get_parameter_bool(self, section, key):
        return bool(self.get_parameter_int(section, key))


if __name__ == '__main__':
    config = ConfigReader('../config/evaluator.ini')
    print config['path', 'filename', 'string']
    print config['path', 'train_filename', 'string']