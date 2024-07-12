import { Body, Controller, Post } from '@nestjs/common';
import { ApiBadRequestResponse, ApiBearerAuth, ApiBody, ApiCreatedResponse, ApiExtraModels, ApiTags, getSchemaPath } from '@nestjs/swagger';
import { WatermarkService } from '../services/watermark.service';
import WatermarkCreateDto from '../dtos/watermark-create.dto';

@ApiTags('file')
@Controller({
  path: 'watermark',
  version: '1',
})
export class WatermarkController {
  constructor(
    private readonly watermarkService: WatermarkService,
  ) {}

  @ApiBearerAuth()
  @ApiBadRequestResponse()
  @ApiCreatedResponse({description: 'Watermark creation process has started successfully'})
  @ApiBody({ type: WatermarkCreateDto })
  @Post('create')
  async createWatermarkInsert(@Body() dto: WatermarkCreateDto): Promise<void> {
    await this.watermarkService.createWatermark(dto);
  }

}
