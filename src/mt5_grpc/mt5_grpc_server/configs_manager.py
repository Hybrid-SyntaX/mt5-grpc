import json
import logging


class ConfigsManager:
    def __init__(self, config_filepath, args):
        self.args = args
        with open(config_filepath) as config_file:
            configs = json.load(config_file)
            self.configs = configs

    def get_node_configs(self):
        if self.args.node_index is not None:
            node_configs = self.configs['nodes'][self.args.node_index]

            if node_configs is not None:
                logging.info(f'Loading configs from node index {self.args.node_index}')
        elif self.args.node_name:
            try:
                node_configs = next(filter(lambda n: n['name'] == self.args.node_name, self.configs['nodes']))
            except StopIteration:
                logging.error(f'[ConfigsManager] Node name `{self.args.node_name}` not found')
                exit(-1)


            if node_configs is not None:
                logging.info(f'Loading configs from node name `{self.args.node_name}`')
        elif self.args.host and self.args.port and self.args.mt_login and self.args.mt_password and self.args.mt_server and self.args.mt_path:
            node_configs = self.generate_configs_from_args()

            if node_configs is not None:
                logging.info(f'Loading configs args')
        else:
            node_configs = self.configs.get('nodes')[0]

            if node_configs is not None:
                logging.info(f'Loading configs node 0 (default)')

        return node_configs

    def generate_configs_from_args(self):
        return {
            'metatrader': {'server': self.args.mt_server,
                           'login': self.args.mt_login,
                           'password': self.args.mt_password,
                           'path': self.args.mt_path},
            'server': {'host': self.args.host, 'port': self.args.port}
        }
