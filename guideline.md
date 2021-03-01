# Content guideline

## General

- While writing the challenge keep in mind that the target group is rookie developers, make sure everything is understandable.
- Correctly name the exercise, make sure that the name is unique, related to the exercise, but not too general. Also keep an eye out for name collisions.
- Provide a comprehensive lessons learned section: summarize what the user learned, what was the vulnerability, why it is dangerous, how can it be prevented, etc.
- Follow [writing guideline](Avatao%20Writing%20Style%20Guide.pdf), grammar, formatting, introduction, message flow
- Avoid external links - let's keep the users on the platform. If a reference is needed show it in the webIDE instead
- As part of the review process all new tutorials must pass a UX research evaluation and content developer (self-)evaluation as well with a 4+ out of 5 score
- Each exercise must have a straightforward takeaway, it should be clear to the user what they just learned

## Technical details

- Pin installed software versions.
- Keep the Dockerfile clean of unnecessary parts, keep the layers optimized
- Provide necessary boilerplate code, don't have the user write it
- Show why the vulnerability is dangerous, it is important that the user understands why we are teaching them the given topic
- Explain the vulnerability to the user before exploiting it and explain the process of fixing
- Make sure that both the code and vulnerability is life-like
- Make sure that the exercise never freezes and the bot always progresses
- The bot should be flexible when it comes to accepting solutions, always prefer unit tests over string matching for example

## Metadata

- Always have hints available
- Make sure correct skill tags are assigned to the tutorial
