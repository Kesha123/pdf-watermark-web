import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe, VersioningType } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { ConfigService } from '@nestjs/config';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));

  app.enableCors();

  app.enableVersioning({
    type: VersioningType.URI,
  });

  const apiDocumentBuilder = new DocumentBuilder()
    .setTitle('PDF Waternark API')
    .setDescription('The documentation provides examples and schemas for PDF Watermark API')
    .setVersion('0.1.0')
    .addBearerAuth()
    .addSecurity('basic', {
      type: 'http',
      scheme: 'mutual',
    })
    .addServer(
      'http://localhost:8000',
      'Localhost - Host to use for local development',
    )
    .addServer(
      'https://api.pdf-watermark.innokentii.eu',
      'Production - Host to use with production environment',
    )
    .build();

  const apiDocument = SwaggerModule.createDocument(app, apiDocumentBuilder, {
    operationIdFactory: (controllerKey: string, methodKey: string) =>
      `${controllerKey}.${methodKey}`,
  });

  SwaggerModule.setup('docs', app, apiDocument);

  const configService = app.get(ConfigService);
  await app.listen(configService.getOrThrow<number>('PORT'));
}
bootstrap();
