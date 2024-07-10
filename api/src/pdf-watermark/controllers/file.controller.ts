import { Body, Controller, Post } from '@nestjs/common';
import { ApiBadRequestResponse, ApiBearerAuth, ApiBody, ApiOkResponse, ApiTags } from '@nestjs/swagger';
import { FileService } from '../services/file.service';
import UploadFileSignedUrlDto from '../dtos/upload-file-signed-url.dto';
import UploadFileDto from '../dtos/upload-file.dto';

@ApiTags('file')
@Controller({
  path: 'file',
  version: '1',
})
export class FileController {
  constructor(
    private readonly fileService: FileService,
  ) {}

  /**
   * Creates a signed URL to upload a file to the S3 bucket
   * @param uploadFileDto
   * @returns A signed URL to upload a file to the S3 bucket
   */
  @ApiBearerAuth()
  @ApiOkResponse({type: UploadFileSignedUrlDto, description: 'Returns a signed URL to upload a file to the S3 bucket'})
  @ApiBadRequestResponse()
  @ApiBody({type: UploadFileDto})
  @Post('get-upload-url')
  async getUploadUrl(@Body() uploadFileDto: UploadFileDto): Promise<UploadFileSignedUrlDto> {
    const signedUrl = await this.fileService.getUploadUrl(uploadFileDto.fileKey);
    const response = new UploadFileSignedUrlDto();
    response.signedUrl = signedUrl;
    return response;
  }

}
