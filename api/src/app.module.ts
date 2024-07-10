import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PdfWatermarkModule } from './pdf-watermark/pdf-watermark.module';

@Module({
  imports: [
    ConfigModule.forRoot(),
    PdfWatermarkModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
