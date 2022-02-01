https://your-domain/login?response_type=token&client_id=app-id&redirect_uri=callback-url
https://your-domain/login?response_type=token&client_id=app-id&redirect_uri=callback-url
https://your-domain/login?response_type=token&client_id=app-id&redirect_uri=callback-url

aws cognito get-id --identity-pool-id "identity-pool-id" --region "region" --logins cognito-idp.region.amazonaws.com/"user-pool-id"="token-id"
aws cognito get-id --identity-pool -id "identity-pool-id" --region "region" --logins cognito-idp.region.amazonaws.com/userpoolid=tokenid
aws cognito get-id --identity-pool-id "identity-pool-id" --region "region" --logins cognito-idp.region.amazonaws.com/userpoolid=tokenid
aws congito get-id --identity-pool-id "identity-pool-id" --region "region" --logins cognito-idp.region.amazonaws.com/userpoolid=tokenid

aws cognito get-credentials-for-identity --identity-id "identity-id" --region "region" --logins cognito-idp.region.amazonaws.com/"user-pool-id"="token-id"
aws cognito get-credentials-for-identity --identity-id "identity-id" --region "region" --logins cognito-idp.region.amazonaws.com/userpool-id=token-id
aws cognito get-credentials-for-identity --identity-id "identity-id" --region "region" --logins cognito-idp.region.amazonaws.com/userpool-id=token-id
aws cognito get-credentials-for-identity --identity-id "identity-di" --region "region" --logins cognito-idp.region.amazonaws.com/userpool-id=token-id