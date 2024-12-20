module.exports = {
	$schema: "https://docs.renovatebot.com/renovate-schema.json",
	extends: [":disableDependencyDashboard"],
	username: "cloudesire-bot",
	gitAuthor: "Victor <cloudesire-dev@eng.it>",
	platform: "github",
	repositories: ["ClouDesire/syndication-python-template"],
	assignees: ["malteo"],
	reviewers: ["malteo"],
	prHourlyLimit: 0,
	prConcurrentLimit: 0,
	branchPrefix: "renovate/",
};
