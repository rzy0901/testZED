function exportGIF(mat_path,output_gif_path,imshow)
clear; close all;
if nargin == 0
    mat_path = './data/temp.mat';
    output_gif_path = './data/temp_mocap.gif';
    imshow = true;
elseif nargin == 1
    output_gif_path = './data/temp_mocap.gif';
    imshow = true;
elseif nargin == 2
    imshow = true;
end
load(mat_path)
keypoints(isnan(keypoints)) = 0;
positions(isnan(positions)) = 0;
velocities(isnan(velocities)) = 0;
% fps =  30;
timestampList = timestampList-timestampList(1);
if size(keypoints,2) == 18
connections = [1 2;2 3;3 4;4 5;2 6;6 7;7 8;3 9;9 10;10 11;6 12;12 13;13 14;3 6;9 12;1 15;15 17;1 16;16 18];
elseif size(keypoints,2) == 34
connections = [1 2; 2 3; 3 5; 5 6; 6 7; 7 8; 8 9;9 10;8 11;3 12;12 13;13 14;14 15;15 16;16 17;15 18;1 19;19 20;20 21;21 22;1 23;23 24;24 25;25 26;3 4;4 27;27 28;28 29;29 30;28 31;31 32;21 33;25 34;33 22;34 26];
elseif size(keypoints,2) == 38
connections = [1 2;2 3;3 4;4 5;5 6;6 7;7 9;6 8;8 10;4 11;11 13;13 15;15 17;17 31;17 33;17 35;17 37;4 12;12 14;14 16;16 18;18 32;18 34;18 36;18 38;1 19;19 21;21 23;23 29;23 25;23 27;1 20;20 22;22 24;24 30;24 26;24 28];
end
hf = figure(1);
hf.Color = 'white';
for ii = 1:1:length(timestampList) % 舍弃第一帧和最后一帧.
    cla
    x = squeeze(keypoints(ii,:,1));
    y = squeeze(keypoints(ii,:,2));
    z = squeeze(keypoints(ii,:,3));
    xmin = min([0 min(keypoints(:,:,1),[],'all')]);
    xmax = max([0 max(keypoints(:,:,1),[],'all')]);
    ymin = min([0 min(keypoints(:,:,2),[],'all')]);
    ymax = max([0 max(keypoints(:,:,2),[],'all')]);
    zmin = min([0 min(keypoints(:,:,3),[],'all')]);
    zmax = max([0 max(keypoints(:,:,3),[],'all')]);
    % plot
    human = scatter3(z,x,y,'filled');
    hold on;
    axis equal;
    xlim([zmin zmax]); % Z
    ylim([xmin xmax]); % X
    zlim([ymin ymax]); % Y
%     xlim([-7 -2]); % 对着相机走
%     ylim([-3 2]) % 垂直相机视角走
    view(30,30)
    camera = scatter3(0,0,0,[],"red",'*','DisplayName','Camera');
    for jj = 1:1:length(connections)
        plot3(z(connections(jj,:)),x(connections(jj,:)),y(connections(jj,:)),'Color','b','LineWidth',0.05);
    end
    xlabel('Z (m)'); ylabel('X (m)'); zlabel('Y (m)'); title(sprintf('Timestamp: %d (ms)',timestampList(ii)));
    grid on;
    legend([camera human] ,'camera','human');
    drawnow;
    if imshow == false
        set(gcf,'Visible','off')
    end
    Frame=getframe(gcf);
    Image=frame2im(Frame);
    [Image,map]=rgb2ind(Image,256);
    if ii == 2
        imwrite(Image,map,output_gif_path,'gif', 'Loopcount',inf,'DelayTime',1/fps);
    else
        imwrite(Image,map,output_gif_path,'gif','WriteMode','append','DelayTime',1/fps);
    end
end
end