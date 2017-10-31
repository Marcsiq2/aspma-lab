function nm = midiWindow(nmat,mintime,maxtime,timetype,clipmode)
% MIDI time-based windowing
% nm = midiwindow(nmat,mintime,maxtime,<timetype>);
% Returns the notes in NMAT whose onset or offset times satisfy
% MINTIME <= onsettime[beats/secs](NMAT) <= MAXTIME
%
% Input arguments:
%	NMAT = notematrix
%	MINTIME = minimum limit of the window in beats (default) or secs
%	MAXTIME = maximum limit of the window in beats (default) or secs
%	TIMETYPE = time representation, 'beat' (default) or 'sec' 
%   CLIPMODE = clip mode, 'clip' (default) or 'noclip'.
%       clip note's begin and/or end according to window (modifies nmat)
%
% Output:
%	NM = notematrix containing the notes of NMAT whose onsets or offsets
%	are within the window
%
% Change History :
% Date		Time	Prog	Note
% 11.8.2002	18:36	PT	Created under MATLAB 5.3 (Macintosh)
%© Part of the MIDI Toolbox, Copyright © 2004, University of Jyvaskyla, Finland
% See License.txt
% 13.9.2010 16:32   adapted from 'onsetwindow' by Agustín Martorell, MTG-UPF

if isempty(nmat), return; end
if nargin <4, timetype = 'beat'; end
if nargin <5, clipmode = 'clip'; end

off_beat = nmat(:,1)+nmat(:,2);
off_sec = nmat(:,6)+nmat(:,7);

if mintime == maxtime, nm = []; return; end
    
if strcmp(timetype, 'beat')==1
	nm = nmat((mintime<=nmat(:,1) & nmat(:,1)<=maxtime) | (mintime<=off_beat & off_beat<=maxtime) | (mintime>nmat(:,1) & maxtime<off_beat),:);
elseif strcmp(timetype, 'sec')==1
	nm = nmat((mintime<=nmat(:,6) & nmat(:,6)<=maxtime) | (mintime<=off_sec & off_sec<=maxtime) | (mintime>nmat(:,6) & maxtime<off_sec),:);
    %          onset within window                         offset within window                    window within note
else
	disp(['Unknown timetype:' timetype])
	disp('Accepted timeformats are ''sec'' or ''beat''! ')
end

on_beat = nm(:,1);
off_beat = nm(:,1)+nm(:,2);
on_sec = nm(:,6);
off_sec = nm(:,6)+nm(:,7);

if strcmp(clipmode, 'clip')==1
    bpm = gettempo(nmat);
    % nmat format = [onset(beats) dur(beats) MIDIchannel MIDInote velocity onset(secs) dur(secs)]
    if strcmp(timetype, 'beat')==1
        nm(:,1) = max(mintime,nm(:,1));
        nm(:,2) = min(off_beat-nm(:,1),maxtime-nm(:,1));
        nm(:,6:7) = [60*nm(:,1)/bpm 60*nm(:,2)/bpm]; % modify info in sec-based fields
    else
        nm(:,6) = max(mintime,nm(:,6));
        nm(:,7) = min(off_sec-nm(:,6),maxtime-nm(:,6));
        nm(:,1:2) = [bpm*nm(:,6)/60 bpm*nm(:,7)/60]; % modify info in beat-based fields
    end
elseif strcmp(clipmode, 'noclip')==1
    return;
else
    disp(['Unknown clipmode:' clipmode])
    disp('Accepted clipmodes are ''clip'' or ''noclip''! ')
end

nm = nm(0<nm(:,2),:); % remove zero-duration events
