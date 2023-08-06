from ronds_sdk.options.pipeline_options import PipelineOptions
from ronds_sdk.runners.runner import PipelineRunner


class PythonRunner(PipelineRunner):

    def __init__(self,
                 options,  # type: PipelineOptions
                 ):
        super(PythonRunner, self).__init__(options)

    def transform_package(self) -> str:
        return "ronds_sdk.transforms.python_dataframe"

    def run_pipeline(self, pipeline, options):
        pass

    def apply(self, transform, input, options):
        pass
