import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { WatermarkController } from './controllers/watermark.controller';
import { FileController } from './controllers/file.controller';
import { FileService } from './services/file.service';
import { WatermarkService } from './services/watermark.service';
import { JwtModule } from '@nestjs/jwt';
import { APP_GUARD } from '@nestjs/core';
import { AuthGuard } from './auth/auth.guard';

@Module({
  imports: [ConfigModule, JwtModule.register({})],
  providers: [FileService, WatermarkService, { provide: APP_GUARD, useClass: AuthGuard }],
  controllers: [WatermarkController, FileController],
})
export class PdfWatermarkModule {}
