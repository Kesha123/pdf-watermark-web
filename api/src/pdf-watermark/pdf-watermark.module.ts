import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { WatermarkController } from './controllers/watermark.controller';
import { FileController } from './controllers/file.controller';
import { FileService } from './services/file.service';
import { WatermarkService } from './services/watermark.service';

@Module({
  imports: [
    ConfigModule,
  ],
  providers: [FileService, WatermarkService],
  controllers: [WatermarkController, FileController]
})
export class PdfWatermarkModule {

}
