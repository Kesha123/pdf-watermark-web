export default class MessageNotCreatedError extends Error {
  constructor() {
    super('MessageNotCreated');
  }
}