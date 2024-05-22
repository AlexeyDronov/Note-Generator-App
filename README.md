# The Idea
This is the very first independent project I have created using some Tkinter and CustomTkinter in Python. 
The idea came from seeing someone on youtube giving advice on how is bes
t to learn every note on the fretboard – 
"Say the notes out loud and play them immediately after on the guitar". 

I wanted to optimise the process, but also was thinking for a while to try myself in creating software, hence this Note Generator.
The app has quite a limited feautere set and is not very well optimised (Python after all), but it made for a nice fortnightly 
project. The user would start the randomiser, look at the note displayed and try to find that note on the fretboard (Now that I think
about it, that would work for ear training on other instruments too...). Each note is accompanied by a note sound played to confirm if the note 
found was correct. 

# Features 
### Time interval
<img width="235" alt="Screenshot 2024-05-22 at 23 41 10" src="https://github.com/AlexeyDronov/Note-Generator-App/assets/58732742/ca8545d5-42b1-498a-97f5-d89246d854d2">

Time interval allows to select an interval with which the notes are randomised (in seconds, from 1 to 30). 

### Note selection
<img width="559" alt="Screenshot 2024-05-22 at 23 42 32" src="https://github.com/AlexeyDronov/Note-Generator-App/assets/58732742/d2b9a152-32f3-4d44-a7fc-a30801342f47">

The user can select which note sets the randomiser draws from. By default it set to a C major scale, however, the user can configure the specific set of notes for the randomiser, 
or use a dropdown menu to select a specific scale

### Number of notes
<img width="385" alt="Screenshot 2024-05-22 at 23 45 12" src="https://github.com/AlexeyDronov/Note-Generator-App/assets/58732742/354dd43e-8c0d-47ec-8c09-99eb609977f9">

The app can show up to 3 notes at a time, for 2 and 3 notes according number of note sounds are played simultaneously. Might be helpful in learning triads.

### Fretboard view
<img width="781" alt="Screenshot 2024-05-22 at 23 46 38" src="https://github.com/AlexeyDronov/Note-Generator-App/assets/58732742/21230bcf-d372-4f22-b82a-ed1e6e30d1b8">

The fretboard view updates with the randomiser showing where the randomised notes are shown on the fretboard.

# Future plans

I will leave the project as it is for now as I'm quite happy with how it turned out, however I have some ideas which were eiter too time consuming to implement,
or required a complete restructuring of the code to be implemented correctly. Cannot say this is the piece of code I'm most proud of, but I have learned a great deal writing it
and I'm sure it'll help me a lot in the future. 

Here are some of those extra ideas:
* Add a toggle between sharps and flats
* Add other modes to be selected from besides Major or Minor (i.e. Dorian, Phrygian, etc.)
* Add an option to display and play chords instead of the notes (+ add sounds to these)
* Create an ear training mode, where the user does not have access to the note displayed and instead only hears the sound
* Add an option to choose bpm instead of seconds as an interval and use metronome

Hope whoever sees it can find some good use in it!
