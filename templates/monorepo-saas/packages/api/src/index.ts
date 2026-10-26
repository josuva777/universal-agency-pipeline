import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string().min(2),
  company: z.string().min(2),
  role: z.enum(['VIEWER', 'DEVELOPER', 'AUDITOR', 'SECURITY_LEAD', 'SUPER_ADMIN']),
  tier: z.enum(['FREE', 'TEAM', 'ENTERPRISE']),
  toolCallsLimit: z.number().int().positive(),
  toolCallsUsed: z.number().int().nonnegative(),
});

export const OTPSendRequestSchema = z.object({
  email: z.string().email(),
});

export const OTPVerifyRequestSchema = z.object({
  email: z.string().email(),
  code: z.string().length(6),
});

export const OTPFinalizeRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2),
  company: z.string().min(2),
});

export type UserDTO = z.infer<typeof UserSchema>;
export type OTPSendRequest = z.infer<typeof OTPSendRequestSchema>;
export type OTPVerifyRequest = z.infer<typeof OTPVerifyRequestSchema>;
export type OTPFinalizeRequest = z.infer<typeof OTPFinalizeRequestSchema>;
