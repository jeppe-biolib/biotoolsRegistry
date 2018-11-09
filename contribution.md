**CAUTION:: WORK IN PROGRESS - EVERYTHING HERE MAY CHANGE**


# Code repo / branch structure
The repo structure follows [branching standards & conventions](https://gist.github.com/digitaljhelms/4287848).  There are two main (permanent) branches ("dev" and "stable"), with other supporting (temporary) branches ("features", "bugfixes" and "hotfixes") with a specific purpose.  Strict rules mandate which branches may be originating branches and which branches must be merge targets.


Instance     | Branch       | Comment
-----------  | ------       | -------
"stable"     | stable       | Accepts merges from "dev" and "hotfixes"
"dev"        | master       | Accepts merges from "features", "bugfixes" and "hotfixes"
"features"   | feature-\<id\> | Always branch off HEAD of "dev"
"bugfixes"   | bugfix-<id>  | Always branch off HEAD of "dev"
"hotfixes"   | hotfix-<id>  | Always branch off "stable"


- **"dev" branch** (`origin/master`) (code deployed on https://dev.bio.tools) 
  - the default / base branch of the repo, against which all pull requests and code commits are automatically made
  - holds changes for the next release
  - core-developers will branch / merge from it
  - accepts pull requests (see Community Development Guidelines below)

- **"stable"** branch (`origin/stable`) (code deployed on https://bio.tools) 
  - latest code deployed to (and allowing bug fixing of) production system
  - not normally interacted with (other than hot fixes)
  - periodically updated from "dev" branch (see Release Process below)
- **"feature"** and **"bug"** branches
  - **"feature"** branches are created for significant new features / enhancements (*i.e.* whose development may take longer than a single deployment) 
  - **"bug"** branches are created to address - in the next deployment - bugs found on the live site (a bug branch typically lasts one deployment cycle only)
  - should always be publicly available (development should never exist in just one developer's local branch)
  - always branch from, and merge back into "dev" branch
  - feature developer (or bug fixer) must watch the "dev" branch for commits, ensuring all changes to it are merged into the feature/bug fix before merging back to "dev" (ideally as one goes along, to make conflict resolution easier)
  - branch naming convention, where `<id>` is a GitHub issue number (all features and bugs should be tracked as GitHub issues):

    - `feature-<id>`
    - `bug-<id>`

- **"hotfix"** branches
  - created when there's a need to immediately fix a problem with the production system (changes can be pushed any time, outside of scheduled deployment)
  - always branch from "stable" (and tag the branch), and merge back into both "stable" and "dev"

    - development of "dev" can continue while the hotfix is being addressed
    - tagged stable branch still represents what is in production.
    
  - branch naming convention:

    - `hotfix-<id>`

# Release process

# Community development guidelines


# Community code of conduct

This code of conduct outlines our expectations for the bio.tools developer community.  It is based loosely on the [GCCBOSC 2018 Code of Conduct](https://galaxyproject.org/events/gccbosc2018/code-of-conduct/#gccbosc-2018-code-of-conduct).  We are committed to providing a welcoming and productive community for all and expect our code of conduct to be honored.  Our open source community strives to be:

- **Considerate:** You depend upon the work of others who in turn depend on you.  You're unlikely to be fully aware of the ramifications of your proposals or actions, and the constraints others work under.  Before deciding or acting, talk to others and reach a common understanding of the consequences. 
- **Constructive:** We will not agree all the time.  Where we disagree, try to understand why and maintain a positive attitude in seeking a resolution, bearing in mind we share a common goal.
- **Supportive:**  Support others in their work (you depend on them!), respecting the fact that we have different levels of experience and technical ability.
- **Open-minded:** We have a wide range of backgrounds, skills and perspectives -  this diversity is a strength.  Be wary of ignoring or misunderstanding another viewpoint in the vindication of your own.
- **Respectful:** Disagreement and differences do not excuse bad manners. Never allow frustration to turn into aggressive conduct or a personal attack.  A happy atmosphere is a productive one:  be nice, and keep a sense of humour.  If you can't be nice, be quiet.
- **Tolerant:**  Treat people fairly and equally irrespective of their background and identity, including technical ability, experience, education, race, gender, nationality, age *etc*.
- **Wise:** We are not infallible; we will make mistakes and change our viewpoints: admit and learn from mistakes and allow others to do the same.  

## Conflict resolution
If you are unhappy in regard to the code of conduct not being honoured, you should raise your concerns immediately and try to resolve them, either directly with the person concerned, or failing that with the nominated community leader (currently [Jon Ison](mailto:jison@bioinformatics.dtu.dk)) who will try to resolve the issue discretely and fairly. 