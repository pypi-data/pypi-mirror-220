
import logging
import os

from mlservicewrapper.core import contexts, server, services
from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer

__all__ = ["ApplicationInsightsLoggingService"]

class ApplicationInsightsLoggingService(services.Service):
    def __init__(self, base_instance: server.SafeServiceWrapper) -> None:
        super().__init__()
        self._base_instance = base_instance

    def _ensure_has_handler(self, logger: logging.Logger):
        if self.__azure_handler is None:
            return
        
        if self.__azure_handler in logger.handlers:
            return
        
        logger.addHandler(self.__azure_handler)

    async def load(self, ctx: contexts.ServiceContext):

        config_integration.trace_integrations(['logging'])

        connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
        
        if connection_string is None:
            connection_string = ctx.get_parameter_value("ApplicationInsightsConnectionString", required=False)

        if connection_string is None:
            logging.warn("Application Insights is not enabled, set the ApplicationInsightsConnectionString parameter to capture logs.")

            self.__azure_handler = None
        else:
            self.__azure_handler = AzureLogHandler(connection_string=connection_string)

            tracer_exporter = AzureExporter(connection_string=connection_string)
            self.__tracer = Tracer(exporter=tracer_exporter, sampler=AlwaysOnSampler())
            
            metrics_exporter.new_metrics_exporter(connection_string=connection_string)
            
            self._ensure_has_handler(ctx.logger)
        
        return await self._base_instance.load(ctx)

    async def process(self, ctx: contexts.ProcessContext):
        if self.__azure_handler is None:
            await self._base_instance.process(ctx)
            return
        
        self._ensure_has_handler(ctx.logger)

        with self.__tracer.span(name="process") as tracer_span:
            tracer_span.span_kind = SpanKind.SERVER

            try:
                await self._base_instance.process(ctx)
            except Exception as ex:
                ctx.logger.exception(str(ex))
                raise

    def dispose(self):
        if self.__azure_handler is not None:
            self.__azure_handler.flush()
            self.__azure_handler.close()

        return self._base_instance.dispose()
