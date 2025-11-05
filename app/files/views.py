import boto3
import hashlib
import datetime
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from botocore.client import Config
from .models import FileMetadata
from .serializers import FileMetadataSerializer


def get_s3_client(internal=True):
    """
    Return an initialized MinIO (S3-compatible) client.
    internal=True → uses 'minio:9000' (inside Docker network)
    internal=False → uses 'localhost:9000' (for host access)
    """
    endpoint = "http://minio:9000" if internal else "http://localhost:9000"
    print(f"[DEBUG] Connecting to MinIO endpoint: {endpoint}")

    try:
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.MINIO_STORAGE_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_STORAGE_SECRET_KEY,
            endpoint_url=endpoint,
            region_name="us-east-1",
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"}
            ),
        )
        print(f"[DEBUG] ✅ boto3 client initialized successfully ({'internal' if internal else 'external'})")
        return client
    except Exception as e:
        print(f"[ERROR] Failed to initialize boto3 client: {e}")
        raise


def ensure_bucket(s3, bucket_name):
    """Create bucket if it doesn't exist."""
    try:
        s3.head_bucket(Bucket=bucket_name)
    except Exception:
        print(f"[INFO] Creating bucket: {bucket_name}")
        s3.create_bucket(Bucket=bucket_name)


class FileUploadView(views.APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        s3 = get_s3_client()
        bucket = settings.MINIO_STORAGE_BUCKET_NAME
        ensure_bucket(s3, bucket)

        storage_key = f"{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.name}"
        content_type = file.content_type or "application/octet-stream"

        sha256 = hashlib.sha256()
        for chunk in file.chunks():
            sha256.update(chunk)
        checksum = sha256.hexdigest()

        file.seek(0)
        s3.upload_fileobj(file, bucket, storage_key, ExtraArgs={"ContentType": content_type})

        meta = FileMetadata.objects.create(
            storage_key=storage_key,
            original_name=file.name,
            content_type=content_type,
            size=file.size,
            checksum=checksum,
        )

        return Response(FileMetadataSerializer(meta).data, status=status.HTTP_201_CREATED)


class PresignedURLView(views.APIView):
    def post(self, request):
        filename = request.data.get("filename")
        if not filename:
            return Response({"error": "Filename required"}, status=status.HTTP_400_BAD_REQUEST)

        s3 = get_s3_client()
        bucket = settings.MINIO_STORAGE_BUCKET_NAME
        ensure_bucket(s3, bucket)

        storage_key = f"{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"

        # Generate presigned URL (valid for 5 minutes)
        url = s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket, "Key": storage_key},
            ExpiresIn=300,
        )

        # Replace internal hostname with localhost for external use
        public_url = url.replace("http://minio:9000", "http://localhost:9000")

        # Generate a ready-to-run curl command
        curl_cmd = f'curl -X PUT -T "{filename}" "{public_url}"'

        print(f"[DEBUG] Generated presigned URL for localhost: {public_url}")

        return Response({
            "upload_url": public_url,
            "storage_key": storage_key,
            "curl_command": curl_cmd
        })


