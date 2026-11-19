# Folder 6 – Software Testing Tools: Bug Fix and Retest

**Application:** Word Scramble game (Pygame), assigned repo `SETAPESU26/62_scramble`
**AI tool used:** GitHub Copilot (VS Code)

## Evidence
- Before (bug visible): https://github.com/ManojGaonkar05/62_scramble/blob/main/Lab-4/Before.mp4
- After (bug fixed, features working): https://github.com/ManojGaonkar05/62_scramble/blob/main/Lab-4/After.mp4
- Chat history with Copilot: https://github.com/ManojGaonkar05/62_scramble/tree/main/Lab-4

## The bug, the cause and the fix
- **Bug:** Typing the correct unscrambled word was rejected, and typing the scrambled letters was accepted as correct.
- **Cause:** The guess was compared against the scrambled display text instead of the actual secret word.
- **Fix:** The guess validation now compares the player's input with the secret target word.

## Features added with AI assistance
- Progressive hint system with a score penalty
- Countdown timer bar that reveals the word and moves to the next round on timeout
- Clickable letter tiles that can be rearranged

## Link to my fixed repository
https://github.com/ManojGaonkar05/62_scramble
