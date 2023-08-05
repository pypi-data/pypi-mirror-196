import json
import os
import Config.localconfig.config
from mapilio_kit.commands.process import Command as ProcessCommand
from mapilio_kit.commands.sample_video import Command as SampleCommand

configs = Config.localconfig.config


def process(file, output_dir):
    processing = ProcessCommand()
    sampling = SampleCommand()

    sampling.run(
        vars_args={
            "video_import_path": file,
            "import_path": output_dir,
            "video_sample_interval": 1,
            "force_overwrite": True
        }
    )
    processing.run(
        vars_args={
            "import_path": output_dir,
            "interpolate_directions": True,
            "geotag_source": "gopro_videos",
            "geotag_source_path": file,
        }
    )


if configs.local and configs.gopro_mp4 != "":
    for fname in os.listdir(configs.gopro_mp4):
        if fname.endswith('.MP4'):
            process(configs.gopro_mp4, f"{os.getcwd()}/LocalExports/")
            jsonfile = f"{os.getcwd()}/LocalExports/mapilio_image_description.json"
else:
    jsonfile = configs.jsonfile


def local_images():
    if os.path.isfile(jsonfile):
        with open(jsonfile, "r") as f:
            jsons = json.load(f)
        keys_to_keep = ["fov", "altitude", "longitude", "heading", "latitude", "filename", "deviceModel", "path",
                        "orientation"]
        jsons = jsons[:-1]
        for i in jsons:
            for key in list(i.keys()):
                if key not in keys_to_keep:
                    del i[key]

            i["coordy"] = i["latitude"]
            i["coordx"] = i["longitude"]
            i["imgname"] = i["filename"]
            del i["latitude"], i["longitude"], i["filename"]

        return jsons, [jsons[0]["coordx"], jsons[0]["coordy"]]
