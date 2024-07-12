import { Injectable } from '@nestjs/common';
import WatermarkCreateDto from '../dtos/watermark-create.dto';
import * as aws from 'aws-sdk';
import { ConfigService } from '@nestjs/config';
import MessageNotCreatedError from '../errors/message-not-created.error';

@Injectable()
export class WatermarkService {
  private sqs: aws.SQS;

  constructor(
    private readonly configService: ConfigService,
  ) {
    aws.config.update({
      region: this.configService.getOrThrow<string>('AWS_REGION'),
    });
    this.sqs = new aws.SQS();
  }


  async createWatermark(dto: WatermarkCreateDto): Promise<void> {
    const messageParams = {
      MessageBody: JSON.stringify(dto),
      QueueUrl: this.configService.getOrThrow<string>('AWS_SQS_URL'),
    };
    try {
      await this.sqs.sendMessage(messageParams).promise();
    } catch (error) {
      console.log(error)
      throw new MessageNotCreatedError();
    }
  }
}
