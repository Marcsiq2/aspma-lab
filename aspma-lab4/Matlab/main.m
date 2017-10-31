clear all; close all; clc

%% read midifile
file = '../Files/original/Sleeper.mid';
addpath('miditoolbox/miditoolbox');
[nmat, ~] = readmidi(file);


%% cut just the Intro and get different parts
intro = onsetwindow(nmat,0,67,'sec');
melody_intro = getmidich(intro, 8);
main_piano_intro = getmidich(intro, 14);
bass_piano_intro = getmidich(intro, 15);
piano_intro = vertcat(main_piano_intro, bass_piano_intro);
mypianoroll(vertcat(piano_intro, melody_intro), 'sec');


%% Compute cord pregression for piano accompaniement
window_size = 2; %in seconds
window_hop_size = 2; %in seconds
keys = movewindow(piano_intro,window_size,window_hop_size,'sec','maxkkcc');
label=keyname(movewindow(piano_intro,window_size,window_hop_size,'sec','kkkey'));
time=0:window_hop_size:floor(length(keys)*window_hop_size)-1; 
plot(time,keys,':ko','LineWidth',1.25);
axis([-0.2 length(keys)*window_hop_size .4 1])
for i=1:length(label)
    text(time(i),keys(i)+.025,label(i),...
    'HorizontalAlignment','center','FontSize',12);

end
ylabel('\bfMax. key corr. coeff.');
xlabel('\bfTime (sec)')

%% Compute cord pregression for piano + melocy
window_size = 2; %in seconds
window_hop_size = 2; %in seconds
keys = movewindow(vertcat(piano_intro, melody_intro),window_size,window_hop_size,'sec','maxkkcc');
label=keyname(movewindow(vertcat(piano_intro, melody_intro),window_size,window_hop_size,'sec','kkkey'));
time=0:window_hop_size:floor(length(keys)*window_hop_size)-1; 
plot(time,keys,':ko','LineWidth',1.25);
axis([-0.2 length(keys)*window_hop_size .4 1])
for i=1:length(label)
    text(time(i),keys(i)+.025,label(i),...
    'HorizontalAlignment','center','FontSize',12);

end
ylabel('\bfMax. key corr. coeff.');
xlabel('\bfTime (sec)')


%% Compute overall key for piano intro
keysom(piano_intro,1);

%% Compute overall key for melody intro
keysom(melody_intro, 1);

%% Compute overall key for piano + melody intro
keysom(vertcat(piano_intro, melody_intro), 1);

%% Compute onset distribution for piano intro
onsetdist(piano_intro,3,'fig');

%% Compute onset distribution for melody intro
onsetdist(melody_intro, 3, 'fig');

%% Compute gestalt segmentation for melody intro
segmentgestalt(melody_intro,'fig');

%% keyspace
keyspace(piano_intro)