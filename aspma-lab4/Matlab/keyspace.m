function [ keysca ] = keyspace( nmat )
%KEYSPACE Summary of this function goes here
%   Detailed explanation goes here
[maxA, ind] = max(nmat(:,6)); %get maximum onset
maxA = ceil(maxA + nmat(ind,7)); %sum duration

keysca = zeros(1,maxA);
last_length=1;
ind = 1;
for i=1:1:maxA
    keys = movewindow(nmat,i,i,'sec','maxkkcc');
    label = movewindow(nmat,i,i,'sec','kkkey');
    disp(length(label));
    w = floor(maxA/length(label));
    a = 1;
    if length(label) ~= last_length
        last_length = length(label);
        ind = ind+1;
        for j = 1:length(label)
            keysca(ind,a:a+w) = label(j);
            a = a+w;
        end
    end
    
end
imagesc(keysca);
set(gca, 'Ydir', 'normal');
grid off;

shading flat;
