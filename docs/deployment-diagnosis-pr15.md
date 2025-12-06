# PR #15 – Vercel preview deployment failure

This environment does not have access to the Vercel dashboard or deployment logs. As a result, the root cause of the preview deployment failure cannot be collected directly here. To diagnose the failure:

1. Open the PR #15 Checks tab in GitHub and follow the Vercel preview link, or open the corresponding deployment in the Vercel dashboard.
2. Scroll to the end of the **Build Logs** after `Deploying outputs...` and copy the last 40–80 lines where the failure is reported.
3. If the build logs end without an error, inspect the **Functions/Runtime Logs** for the same deployment to capture any runtime initialization errors that cause the deployment to be marked as failed.

Once the logs are captured, we can classify the failure as configuration, build artifact, or runtime and patch accordingly.
