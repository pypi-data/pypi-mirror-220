from typing import Any, List, Optional, Union

from pydantic import BaseModel

from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration


class KinesisSource(StreamSource, BaseModel, frozen=True):
    region_name: str
    """
    AWS region string, e.g. "us-east-2". Required,
    """

    stream_name: Optional[Union[str, List[str]]] = None
    """The name of your stream. Either this or the stream_arn must be specified"""

    stream_arn: Optional[Union[str, List[str]]] = None
    """The ARN of your stream. Either this or the stream_name must be specified"""

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_stream_name: Optional[str] = None
    """
    Kinesis stream name to send messages when message processing fails
    """

    aws_access_key_id: Optional[str] = None
    """
    AWS access key id credential
    """

    aws_secret_access_key: Optional[str] = None
    """
    AWS secret access key credential
    """

    aws_session_token: Optional[str] = None
    """
    AWS access key id credential
    """

    endpoint_url: Optional[str] = None
    """
    optional endpoint to hit Kinesis server
    """

    def __init__(
        self,
        *,
        region_name: str,
        stream_name: Optional[str] = None,
        stream_arn: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_stream_name: Optional[str] = None,
        name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        endpoint_url: Optional[str] = None,
    ):
        if stream_name is None and stream_arn is None:
            raise ValueError(f"Kinesis source {name} must have either a stream name or stream ARN specified.")
        super(KinesisSource, self).__init__(
            stream_name=stream_name,
            stream_arn=stream_arn,
            name=name,
            late_arrival_deadline=late_arrival_deadline,
            dead_letter_queue_stream_name=dead_letter_queue_stream_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )

    def _config_to_json(self) -> Any:
        return self.json()

    @property
    def streaming_type(self) -> str:
        return "kinesis"

    @property
    def dlq_name(self) -> Union[str, None]:
        return self.dead_letter_queue_stream_name
