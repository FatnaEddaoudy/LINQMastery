import { Octokit } from '@octokit/rest';

let connectionSettings: any;

async function getAccessToken() {
  if (connectionSettings && connectionSettings.settings.expires_at && new Date(connectionSettings.settings.expires_at).getTime() > Date.now()) {
    return connectionSettings.settings.access_token;
  }
  
  const hostname = process.env.REPLIT_CONNECTORS_HOSTNAME
  const xReplitToken = process.env.REPL_IDENTITY 
    ? 'repl ' + process.env.REPL_IDENTITY 
    : process.env.WEB_REPL_RENEWAL 
    ? 'depl ' + process.env.WEB_REPL_RENEWAL 
    : null;

  if (!xReplitToken) {
    throw new Error('X_REPLIT_TOKEN not found for repl/depl');
  }

  connectionSettings = await fetch(
    'https://' + hostname + '/api/v2/connection?include_secrets=true&connector_names=github',
    {
      headers: {
        'Accept': 'application/json',
        'X_REPLIT_TOKEN': xReplitToken
      }
    }
  ).then(res => res.json()).then(data => data.items?.[0]);

  const accessToken = connectionSettings?.settings?.access_token || connectionSettings.settings?.oauth?.credentials?.access_token;

  if (!connectionSettings || !accessToken) {
    throw new Error('GitHub not connected');
  }
  return accessToken;
}

async function getUncachableGitHubClient() {
  const accessToken = await getAccessToken();
  return new Octokit({ auth: accessToken });
}

async function createRepository(repoName: string, description: string, isPrivate: boolean = false) {
  const octokit = await getUncachableGitHubClient();
  
  try {
    const { data: user } = await octokit.users.getAuthenticated();
    console.log(`Authenticated as: ${user.login}`);
    
    const { data: repo } = await octokit.repos.createForAuthenticatedUser({
      name: repoName,
      description: description,
      private: isPrivate,
      auto_init: false
    });
    
    console.log(`\n✅ Repository created successfully!`);
    console.log(`Repository URL: ${repo.html_url}`);
    console.log(`Clone URL: ${repo.clone_url}`);
    console.log(`\nTo push your code, run these commands in the Shell:`);
    console.log(`\ngit init`);
    console.log(`git add .`);
    console.log(`git commit -m "Initial commit: HR CV Matcher application"`);
    console.log(`git branch -M main`);
    console.log(`git remote add origin ${repo.clone_url}`);
    console.log(`git push -u origin main\n`);
    
    return repo;
  } catch (error: any) {
    if (error.status === 422) {
      console.error(`❌ Error: Repository '${repoName}' already exists in your account.`);
      console.error(`Please choose a different name or delete the existing repository.`);
    } else {
      console.error(`❌ Error creating repository:`, error.message);
    }
    throw error;
  }
}

const repoName = process.argv[2] || 'hr-cv-matcher';
const description = process.argv[3] || 'HR CV Matcher - AI-powered candidate matching application with NLP-based skills extraction';
const isPrivate = process.argv[4] === 'true';

createRepository(repoName, description, isPrivate).catch(console.error);
