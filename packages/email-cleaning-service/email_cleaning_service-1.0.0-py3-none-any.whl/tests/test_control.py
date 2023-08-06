from email_cleaning_service.control import EmailCleaner
from email_cleaning_service.utils.request_classes import PipelineSpecs, RunSpecs, EncoderSpecs
import pytest

tracking_uri = "https://mentis.io/mlflow/"
storage_uri = "tests/test_data/"


def test_segmenting_service():

    emailCleaner = EmailCleaner(tracking_uri=tracking_uri, storage_uri=storage_uri)

    # Example of how to segment a dataset

    thread_list = [
        "This is a test email. I am testing the email cleaner.",
        "This is another test email with two lines.\n I am testing the email cleaner.",
    ]

    pipeline_specs = PipelineSpecs(
        classifier_origin="h5",
        classifier_id="./tests/test_data/base_multi_miniLM_classifier_optimized/multi_miniLM_classifier.h5",
        encoder_origin="hugg",
        encoder_id="sentence-transformers/paraphrase-MiniLM-L12-v2",
        encoder_dim=384,
        features=[
            "phone_number",
            "url",
            "punctuation",
            "horizontal_separator",
            "hashtag",
            "pipe",
            "email",
            "capitalized",
            "full_caps"
        ])

    dataset = emailCleaner.segment(thread_list, pipeline_specs)
    assert len(dataset.threads) == 2

@pytest.mark.skip(reason="too long")
def test_encoder_training_service():

    emailCleaner = EmailCleaner(tracking_uri=tracking_uri, storage_uri=storage_uri)

    # Example of how to train a classifier

    dataset = RunSpecs(
        run_name="test_run_2",
        csv_train="./test_data/test_en.csv",
        csv_test="./test_data/test_en.csv",
        batch_size=2,
        metrics=["seq_f1", "frag_f1"],
        lr=0.001,
        epochs=1,
    )

    encoder_specs = EncoderSpecs(
        origin="mlflow",
        encoder="4f79fbb76bfb44c292a354e2cca5736e",
    )

    emailCleaner.train_encoder(dataset, encoder_specs=encoder_specs)
    assert True

@pytest.mark.skip(reason="too long")
def test_classifier_training_service():

    emailCleaner = EmailCleaner(tracking_uri=tracking_uri, storage_uri=storage_uri)

    # Example of how to train a classifier

    dataset = RunSpecs(
        run_name="test_run_2",
        csv_train="/test_data/test_en.csv",
        csv_test="/test_data/test_en.csv",
        batch_size=2,
        metrics=["seq_f1", "frag_f1"],
        lr=0.01,
        epochs=1,
    )

    pipeline_specs = PipelineSpecs(
        origin="hugg",
        classifier_id="a1f66311816e417cb94db7c2457b25d1"
    )

    emailCleaner.train_classifier(dataset, pipeline_specs)
    assert True

if __name__ == "__main__":
    test_segmenting_service()
    test_encoder_training_service()
    test_classifier_training_service()

