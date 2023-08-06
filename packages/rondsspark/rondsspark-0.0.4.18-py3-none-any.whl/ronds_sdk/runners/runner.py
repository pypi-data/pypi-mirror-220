import importlib
from typing import Optional

from ronds_sdk.options.pipeline_options import PipelineOptions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk.pipeline import Pipeline
    from ronds_sdk.transforms.ptransform import PTransform
    from ronds_sdk.dataframe import pvalue


class PipelineRunner(object):

    def __init__(self,
                 options  # type: PipelineOptions
                 ):
        self._options = options if options else PipelineOptions()
        self.mod = None

    @property
    def options(self):
        return self._options

    def transform_package(self) -> str:
        raise NotImplementedError(
            'runner [%s] must implement transform_package' % self.__class__.__name__)

    def run(self,
            transform,  # type: PTransform
            options=None
            ):
        # type: (...) -> PipelineResult

        """Run the given transform or callable with this runner.

        Blocks until the pipeline is complete.  See also `PipelineRunner.run_async`.
        """
        result = self.run_async(transform, options)
        result.wait_until_finish()
        return result

    def run_async(self,
                  transform,  # type: PTransform
                  options=None
                  ):
        # type: (...) -> PipelineResult
        from ronds_sdk.pipeline import Pipeline
        p = Pipeline(runner=self, options=options)
        if isinstance(transform, PTransform):
            p | transform
        return p.run()

    def run_pipeline(self,
                     pipeline,  # type: Pipeline
                     options  # type: PipelineOptions
                     ):
        # type: (...) -> PipelineResult
        """Execute the entire pipeline or the sub-DAG reachable from a node.
        Runners should override this method.
        """
        raise NotImplementedError

    def apply(self,
              transform,  # type: PTransform
              input,  # type: Optional[pvalue.PValue]
              options  # type: PipelineOptions
              ):
        """Runner callback for a pipeline.apply call."""
        raise NotImplementedError(
            'Execution of [%s] not implemented in runner %s.' % (transform, self))


class PipelineResult(object):
    """A :class:`PipelineResult` 提供获取 pipelines 的信息获取"""

    def __init__(self, state):
        self._state = state

    def state(self):
        """返回当前的 pipelines 执行状态信息"""
        return self._state

    def wait_until_finish(self, duration=None):
        """
        等待 pipelines 运行结束,返回最终状态
        :param duration: 等待时间 (milliseconds). 若设置为 :data:`None`, 会无限等待
        :return: 最终的任务执行状态,或者 :data:`None` 表示超时
        """
        raise NotImplementedError
