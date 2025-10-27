# Myk's Claude Skills
This repo contains a few things I've been playing with. Each skill has its own top-level folder, the most recent build is in `<skill_name>/dist/<skill_name>.skill`. You can use them with a paid claude account - go into `settings` -> `capabilities` -> `skills`, upload a new skill, and upload the .skill file. From there you should be able to use them in claude conversations.

## Domain-Agnostic Operational Composer 
This one is weird and powerful, but quite experimental. The basic idea is that there are all kinds of different domains of knowledge out there, each with its own "operations" -- think, like, the way software engineering has "unit testing", or music theory has "counterpoint", or math has "derivatives". The key insight behind the DAOC skill is that while we tend to think of operations as belonging to domains, any given operation is itself constrained not by the semantics of its domain but by the structure of its inputs.

What this means is that in theory, given some complex problem with a bunch of complicated constraints, Claude can analyze the problem in terms of its structure and then try to identify operations from arbitrary domains that are designed to solve problems with a similar structure. It can then pull in these operations and compose them together to find novel approaches to solving your problem. Give it a try!

[⬇️ Download DAOC.skill](./daoc/dist/daoc.skill)

## Custom Tarot Designer
This one is more just fun. The idea is that Tarot works because it has a specific structure onto which certain archetypal semantics are projected. But what if we can get Claude to preserve that structure while replacing the semantics entirely?

So this tool has Claude ask you for a theme, and then work with you following a specific approach to create theme-specific suits, a novel Major Arcana based on your theme, and then ranks and face cards. It assigns meanings to both suits and ranks, so that each card exists at the intersection of suit meanings and rank meanings.

Then it gives you a JSON file containing your deck, and it opens an interface where you can upload that JSON file to explore it. As a bonus, using the interface you can have claude design interactive animated images for each card using P5.js. This means we're not using image-gen AI tools (which are often trained on stolen artworks and at least to me introduce a world of ethical complexity), we're actually allowing Claude to be creative and code up the visuals. You can use the default prompt, or you can customize it.

Then you can deal yourself spreads and have Claude interpret them for you!
[⬇️ Download tarot.skill](./tarot/dist/tarot.skill)
