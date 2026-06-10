With XCode 27 beta the most recent version of Copilot CLI gives an error when setup using "copilot --acp --stdio" mode. Version is not being passed in from XCode. This python script provides a working bridge.

Apple Engineers provided an update:  use "--acp" without the --stdio argument.  And I can confirm that indeed works, obviating the need for this script!

<img width="477" height="607" alt="Screenshot 2026-06-10 at 4 08 15 PM" src="https://github.com/user-attachments/assets/1fd597a9-c5dc-4436-bb0d-feab1cd4e523" />
