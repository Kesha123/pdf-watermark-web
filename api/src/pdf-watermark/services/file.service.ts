import { PutObjectCommand, S3Client } from '@aws-sdk/client-s3';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import MissingConfigurationError from '../errors/missing-configuration.error';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

@Injectable()
export class FileService {
  private awsS3Client: S3Client;
  private awsS3BucketName: string;
  private awsS3Region: string;

  constructor(
    private readonly configService: ConfigService,
  ) {
    try {
      this.awsS3BucketName = configService.getOrThrow<string>('AWS_S3_BUCKET_NAME');
      this.awsS3Region = configService.getOrThrow<string>('AWS_S3_REGION');
    } catch (error) {
      throw new MissingConfigurationError();
    }
    this.awsS3Client = new S3Client({
      region: this.awsS3Region,
    });
  }

  /**
   * Generates a signed URL to upload a file to the S3 bucket
   * @param fileKey
   * @returns A url to upload a file to the S3 bucket
   */
  async getUploadUrl(fileKey: string): Promise<string> {
    const uploadObjectParams = new PutObjectCommand({
      Bucket: this.awsS3BucketName,
      Key: fileKey,
    });
    const url = await getSignedUrl(this.awsS3Client,uploadObjectParams);
    return url;
  }
}
