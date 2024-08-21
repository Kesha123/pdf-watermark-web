routerAdd('POST', '/api/auth/token-validate', (c) => {
  return c.json(200, { message: 'Authorized' })
}, $apis.requireAdminOrRecordAuth());
