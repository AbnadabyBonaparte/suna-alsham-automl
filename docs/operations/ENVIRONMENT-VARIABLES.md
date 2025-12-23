# 🔐 Environment Variables - ALSHAM QUANTUM

**Complete map of all environment variables used in the project.**

---

## 📋 Quick Reference

### Minimum Required (Login/Dashboard)

```env
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sbp_anon_xxx
```

### Full Configuration

```env
# Supabase (Required)
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sbp_anon_xxx
SUPABASE_SERVICE_ROLE_KEY=sbp_service_role_xxx

# Development (Optional)
NEXT_PUBLIC_DEV_MODE=false

# Stripe (If using payments)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# AI Providers (If using AI features)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# GitHub (If using auto-commit)
GITHUB_TOKEN=ghp_xxx
GITHUB_OWNER=AbnadabyBonaparte
GITHUB_REPO=suna-alsham-automl
```

---

## 📊 Complete Variable Table

### Core - Supabase/Auth/Dashboard

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | public | ✅ Critical | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | public | ✅ Critical | Supabase anon key (client) |
| `SUPABASE_SERVICE_ROLE_KEY` | server | ⚠️ For webhooks/scripts | Supabase service role key |
| `NEXT_PUBLIC_DEV_MODE` | public | Optional | Bypass auth for development |

### Payments - Stripe

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | public | For checkout | Stripe publishable key |
| `STRIPE_SECRET_KEY` | server | For checkout | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | server | For webhooks | Stripe webhook signature |

### AI Providers

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `OPENAI_API_KEY` | server | For AI features | OpenAI API key |
| `ANTHROPIC_API_KEY` | server | For evolution | Anthropic (Claude) key |

### GitHub Integration

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `GITHUB_TOKEN` | server | For auto-commit | GitHub personal access token |
| `GITHUB_OWNER` | server | For auto-commit | GitHub username/org |
| `GITHUB_REPO` | server | For auto-commit | Repository name |

---

## 🌍 By Environment

### Local Development (.env.local)

```env
NEXT_PUBLIC_SUPABASE_URL=https://vktzdrsigrdnemdshcdp.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_DEV_MODE=true  # Optional: bypass auth
```

### Vercel Development

```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_DEV_MODE=true
```

### Vercel Preview

```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY
SUPABASE_SERVICE_ROLE_KEY
```

### Vercel Production

```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY
ANTHROPIC_API_KEY
# NEVER set NEXT_PUBLIC_DEV_MODE=true in production!
```

---

## ⚠️ Security Rules

### NEVER Do This

```env
# ❌ NEVER commit to git
SUPABASE_SERVICE_ROLE_KEY=sbp_service_role_xxx

# ❌ NEVER expose as NEXT_PUBLIC_
NEXT_PUBLIC_SERVICE_ROLE_KEY=xxx  # WRONG!

# ❌ NEVER set in production
NEXT_PUBLIC_DEV_MODE=true  # Only for dev/preview
```

### ALWAYS Do This

```env
# ✅ Use .env.local (gitignored)
# ✅ Set server keys in Vercel dashboard only
# ✅ Use different keys for dev/prod
```

---

## 🔧 Supabase Configuration

### Required in Supabase Dashboard

1. **Redirect URLs** (Authentication → URL Configuration):
   - `https://quantum.alshamglobal.com.br/auth/callback` (production)
   - `http://localhost:3000/auth/callback` (development)

2. **RLS Policies**: Enabled on all tables

3. **Triggers**: `on_auth_user_created` for auto-profile creation

---

## ✅ Checklists

### Setting Up Local Environment

- [ ] Copy `frontend/env.example` to `.env.local`
- [ ] Fill `NEXT_PUBLIC_SUPABASE_URL`
- [ ] Fill `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [ ] (Optional) Set `NEXT_PUBLIC_DEV_MODE=true` for bypass
- [ ] Run `npm run dev` to verify

### Setting Up Vercel

- [ ] Add `NEXT_PUBLIC_SUPABASE_URL`
- [ ] Add `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [ ] Add Stripe keys (if using payments)
- [ ] Add `SUPABASE_SERVICE_ROLE_KEY` (server-only)
- [ ] Redeploy after adding variables

### Verifying Configuration

```bash
# In browser console after login:
console.log(process.env.NEXT_PUBLIC_SUPABASE_URL);
// Should show your Supabase URL

# Check for auth token:
localStorage.getItem('sb-vktzdrsigrdnemdshcdp-auth-token');
// Should exist after login
```

---

## 📚 Related Documents

- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [auth-login-failure runbook](./runbooks/auth-login-failure.md) - Login troubleshooting
- Original: `frontend/docs/MAPA_ENVS.md`

---

**Last Updated:** 2025-12-23

