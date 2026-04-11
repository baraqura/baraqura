{
  name: String,
  email: String,
  apiKey: String,
  plan: { type: String, enum: ['FREE', 'PRO', 'BIZ'], default: 'FREE' },
  usage: { current: Number, limit: Number }, // Free = 1000 limit
  billingId: String // Stripe Customer ID
}
