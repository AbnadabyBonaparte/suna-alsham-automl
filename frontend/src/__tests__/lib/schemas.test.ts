import { loginSchema, signupSchema, requestSchema, profileSchema } from '@/lib/schemas';

describe('loginSchema', () => {
  it('should validate correct login data', () => {
    const result = loginSchema.safeParse({
      email: 'user@test.com',
      password: '123456',
    });
    expect(result.success).toBe(true);
  });

  it('should reject invalid email', () => {
    const result = loginSchema.safeParse({
      email: 'not-an-email',
      password: '123456',
    });
    expect(result.success).toBe(false);
  });

  it('should reject short password', () => {
    const result = loginSchema.safeParse({
      email: 'user@test.com',
      password: '12345',
    });
    expect(result.success).toBe(false);
  });
});

describe('signupSchema', () => {
  it('should validate matching passwords', () => {
    const result = signupSchema.safeParse({
      email: 'user@test.com',
      password: '123456',
      confirmPassword: '123456',
    });
    expect(result.success).toBe(true);
  });

  it('should reject mismatched passwords', () => {
    const result = signupSchema.safeParse({
      email: 'user@test.com',
      password: '123456',
      confirmPassword: '654321',
    });
    expect(result.success).toBe(false);
  });
});

describe('requestSchema', () => {
  it('should validate correct request', () => {
    const result = requestSchema.safeParse({
      title: 'Test Request',
      description: 'Some description',
      priority: 'high',
    });
    expect(result.success).toBe(true);
  });

  it('should reject empty title', () => {
    const result = requestSchema.safeParse({
      title: '',
      priority: 'normal',
    });
    expect(result.success).toBe(false);
  });

  it('should default priority to normal', () => {
    const result = requestSchema.safeParse({
      title: 'Test',
    });
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.priority).toBe('normal');
    }
  });
});

describe('profileSchema', () => {
  it('should validate correct profile', () => {
    const result = profileSchema.safeParse({
      full_name: 'John Doe',
      email: 'john@test.com',
      avatar_url: 'https://example.com/avatar.jpg',
    });
    expect(result.success).toBe(true);
  });

  it('should allow null avatar_url', () => {
    const result = profileSchema.safeParse({
      full_name: 'John Doe',
      email: 'john@test.com',
      avatar_url: null,
    });
    expect(result.success).toBe(true);
  });
});
