import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { Request } from 'express';
import { SetMetadata } from '@nestjs/common';
import { CognitoJwtVerifier } from 'aws-jwt-verify';
import { SimpleJwksCache } from 'aws-jwt-verify/jwk';
import { SimpleJsonFetcher } from 'aws-jwt-verify/https';
import { readFileSync } from 'fs';
import * as path from 'path';
import { ConfigService } from '@nestjs/config';

export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private reflector: Reflector, private readonly configService: ConfigService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) {
      return true;
    }
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    if (!token) {
      throw new UnauthorizedException();
    }
    const verifier = CognitoJwtVerifier.create(
      {
        userPoolId: this.configService.getOrThrow<string>('AWS_COGNITO_USER_POOL_ID'),
        tokenUse: 'id',
        clientId: this.configService.getOrThrow<string>('AWS_COGNITO_CLIENT_ID'),
      },
      {
        jwksCache: new SimpleJwksCache({
          fetcher: new SimpleJsonFetcher({
            defaultRequestOptions: {
              responseTimeout: 3000,
            },
          }),
        }),
      },
    );
    const filePath = path.resolve(__dirname, '../assets/', 'jwks.json');
    const jwks = JSON.parse(readFileSync(filePath, { encoding: 'utf-8' }));
    verifier.cacheJwks(jwks);
    try {
      await verifier.verify(token);
    } catch (error) {
      console.log(error);
      throw new UnauthorizedException();
    }
    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
