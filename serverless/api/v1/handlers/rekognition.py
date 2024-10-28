import json
from infra.aws.rekognition import image_processor


# Lambda function that will be invoked by the API Gateway
def lambda_handler(event, context):
    try:
        """Gets the bucket name and image key from the request body"""
        body = json.loads(event.get("body", "{}"))
        bucket_name = body.get("bucket_name")
        image_key = body.get("image_key")

        """Basic field validation"""
        if not bucket_name or not image_key:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "bucket_name and image_key are required"}
                ),
            }

        """Calls the image processor"""
        result = image_processor.process_image(bucket_name, image_key)

        """Returns the result in JSON format"""
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
