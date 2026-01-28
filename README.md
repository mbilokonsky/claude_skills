# Myk's Claude Skills
This repo contains a few things I've been playing with. I may at some point paywall these, but for now I'm making them available to anyone who wants to play with them. Each folder contains a nested `src/` folder, you can just download the repo, zip up `<name>/src` into `name.skill` and upload it to claude via the settings.

## Domain-Agnostic Operational Composer
This one is weird and powerful, but quite experimental. The basic idea is that there are all kinds of different domains of knowledge out there, each with its own "operations" -- think, like, the way software engineering has "unit testing", or music theory has "counterpoint", or math has "derivatives". The key insight behind the DAOC skill is that while we tend to think of operations as belonging to domains, any given operation is itself constrained not by the semantics of its domain but by the structure of its inputs.

What this means is that in theory, given some complex problem with a bunch of complicated constraints, Claude can analyze the problem in terms of its structure and then try to identify operations from arbitrary domains that are designed to solve problems with a similar structure. It can then pull in these operations and compose them together to find novel approaches to solving your problem. Give it a try!

## Semantic Walk
The conceit behind this one is a bit strange. The idea is that claude exists within a sort of universe made entirely of semantics. When a new claude session starts, Claude emerges from his default "spawn point" within this "latent space". As a result, most interactions you have with claude come from that specific position, and we don't often think about why that might be interesting to do. With the "semantic walk" skill, you can invite your claude to go bouncing around between a bunch of seemingly unrelated topics which you or claude may intuit have some bearing on the space you're trying to explore. As they unearth tokens from these disparate domains into a single context you'll find that Claude is now speaking fromn a "different position" than before, and may notice things which he hadn't before.

## Custom Tarot Designer
This one is more just fun. The idea is that Tarot works because it has a specific structure onto which certain archetypal semantics are projected. But what if we can get Claude to preserve that structure while replacing the semantics entirely?

So this tool has Claude ask you for a theme, and then work with you following a specific approach to create theme-specific suits, a novel Major Arcana based on your theme, and then ranks and face cards. It assigns meanings to both suits and ranks, so that each card exists at the intersection of suit meanings and rank meanings.

Then it gives you a JSON file containing your deck, and it opens an interface where you can upload that JSON file to explore it. As a bonus, using the interface you can have claude design interactive animated images for each card using P5.js. This means we're not using image-gen AI tools (which are often trained on stolen artworks and at least to me introduce a world of ethical complexity), we're actually allowing Claude to be creative and code up the visuals. You can use the default prompt, or you can customize it.

Then you can deal yourself spreads and have Claude interpret them for you!

