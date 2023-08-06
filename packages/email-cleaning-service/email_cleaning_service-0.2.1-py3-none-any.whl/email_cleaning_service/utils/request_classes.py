from typing import List, Optional
from pydantic import BaseModel

### Base models ###


class EncoderSpecs(BaseModel):
    origin: str
    encoder: str


class PipelineSpecs(BaseModel):
    classifier_origin: str
    classifier_id: str
    encoder_origin: str
    encoder_id: Optional[str]
    encoder_dim: Optional[int]
    features: Optional[List[str]]


class RunSpecs(BaseModel):
    run_name: str
    csv_train: str
    csv_test: str
    batch_size: int
    metrics: List[str]
    lr: float
    epochs: int


### Request models ###


class SegmentRequest(BaseModel):
    pipeline: PipelineSpecs
    threads: List[str]


class ClassifierTrainRequest(BaseModel):
    run: RunSpecs
    pipeline: PipelineSpecs


class EncoderTrainRequest(BaseModel):
    run: RunSpecs
    encoder: EncoderSpecs
