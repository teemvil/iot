from ExampleSensor.RngSensor import RngSensor
import argparse


def read_config_from_argument():
    all_args = argparse.ArgumentParser()
    all_args.add_argument("-f", "--config", type=argparse.FileType("r"),  required=True,
                          help="Config file to be used.")

    args = vars(all_args.parse_args())
    return args["config"].read()


if __name__ == '__main__':
    config = read_config_from_argument()
    print(config)
    x = RngSensor()
    x.run()
