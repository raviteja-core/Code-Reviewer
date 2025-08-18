# Vercel Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code is committed to Git repository
- [ ] `vercel.json` is present and configured
- [ ] `api/index.py` serverless function is working
- [ ] `api/requirements.txt` contains all dependencies
- [ ] Application runs locally without errors

### 2. Database Setup
- [ ] Supabase project is created
- [ ] Database tables are set up using `supabase_setup.sql`
- [ ] Supabase credentials are ready:
  - [ ] Project URL
  - [ ] Anon/Public key

### 3. API Keys
- [ ] Gemini API key is obtained from Google AI Studio
- [ ] API key has sufficient quota for testing

## 🚀 Deployment Steps

### Step 1: Push to Git
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variables
vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY
vercel env add GEMINI_API_KEY
vercel env add SECRET_KEY
```

#### Option B: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Configure environment variables
5. Deploy

### Step 3: Environment Variables
Set these in Vercel project settings:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anon key
- `GEMINI_API_KEY`: Your Gemini API key
- `SECRET_KEY`: Secure random string for sessions
- `FLASK_ENV`: production

## ✅ Post-Deployment Verification

### 1. Basic Functionality
- [ ] Application loads without errors
- [ ] Home page displays correctly
- [ ] User registration works
- [ ] User login works
- [ ] Dashboard loads

### 2. Core Features
- [ ] Code submission works
- [ ] AI feedback is generated
- [ ] Feedback page displays correctly
- [ ] History page works
- [ ] Database operations work

### 3. Performance
- [ ] Pages load within reasonable time
- [ ] AI processing completes within 30 seconds
- [ ] No timeout errors

## 🔧 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Vercel dashboard
   - Verify all dependencies in `api/requirements.txt`
   - Check Python version compatibility

2. **Environment Variable Errors**
   - Verify all variables are set in Vercel
   - Check variable names match exactly
   - Test with local environment variables

3. **Database Connection Issues**
   - Verify Supabase project is active
   - Check database schema is set up
   - Test Supabase credentials locally

4. **Function Timeouts**
   - AI processing can take time
   - Consider optimizing AI calls
   - Check function logs for errors

## 📊 Monitoring

### Vercel Dashboard
- Monitor function execution times
- Check for errors in function logs
- Monitor bandwidth usage

### Supabase Dashboard
- Monitor database performance
- Check for connection issues
- Review query performance

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ Application is accessible via Vercel URL
- ✅ All core features work correctly
- ✅ Database operations are functional
- ✅ AI feedback generation works
- ✅ No critical errors in logs
- ✅ Performance is acceptable

## 📞 Support

If you encounter issues:
1. Check Vercel function logs
2. Review Supabase dashboard
3. Test locally with same environment variables
4. Check Vercel and Supabase documentation 