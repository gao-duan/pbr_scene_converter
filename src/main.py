from core import MitsubaLoader as mit
from core import PBRTv3Loader as pbrt
from mitsuba import MitsubaToPBRTv3 as mp
from pbrt import PBRTv3ToMitsuba as pm

import sys

import argparse
import os


class SceneType(object):
    def __init__(self, name, suffix, loader, saver):
        self.name = name
        self.suffix = suffix
        self.loader = loader
        self.saver = saver

def insert_type(name, suffix, loader, saver):
    ValidScenes[name] = SceneType(name, suffix, loader, saver)

ValidScenes = {}
insert_type('pbrt_v3', suffix='.pbrt', loader=pbrt.PBRTv3Loader, saver = mp.MitsubaToPBRTv3 )
insert_type('mitsuba', suffix='xml', loader=mit.MitsubaLoader,saver = pm.PBRTv3ToMitsuba)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True)
    parser.add_argument('--mode', type=str, required=True)
    parser.add_argument('--out_file', type=str, default=None)
    args, unknown = parser.parse_known_args()

    args.src_type, args.dst_type = args.mode.split('_to_')

    if args.src_type not in ValidScenes.keys() or args.dst_type not in ValidScenes.keys():
        print("Error: Invalid mode: %s" % args.mode)
        exit(-1) 

    if args.out_file is None:
        base_path, input_name = os.path.split(args.input_file)
        input_base_name = os.path.splitext(input_name)[0]
        suffix = ValidScenes[args.dst_type].suffix

        args.out_file = os.path.join(base_path, input_base_name, suffix)

    os.makedirs(os.path.split(args.out_file)[0], exist_ok=True)
    
    loader = ValidScenes[args.src_type].loader
    saver = ValidScenes[args.dst_type].saver

    scene = loader(args.input_file).scene
    saver(scene, args.out_file)