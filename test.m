clear; clc; close all;
load('./data2/lqr/walk2/walk2_1.mat')

% fps =  30;
timestampList = timestampList-timestampList(1);
connection = [1 2; 2 3; 3 5; 5 6; 6 7; 7 8; 8 9;9 10;8 11;3 12;12 13;13 14;14 15;15 16;16 17;15 18;1 19;19 20;20 21;21 22;1 23;23 24;24 25;25 26;3 4;4 27;27 28;28 29;29 30;28 31;31 32;21 33;25 34;33 22;34 26];
hf = figure(1);
hf.Color = 'white';
for ii = 2:1:length(timestampList)-1 % 舍弃第一帧和最后一帧.
    cla
    x = squeeze(keypoints(ii,:,1));
    y = squeeze(keypoints(ii,:,2));
    z = squeeze(keypoints(ii,:,3));
    % plot
    human = scatter3(z,x,y,'filled');
    hold on;
    axis equal;
%     xlim([-7 -2]); % 对着相机走
%     ylim([-3 2]) % 垂直相机视角走
    view(30,30)
    camera = scatter3(0,0,0,[],"red",'*','DisplayName','Camera');
    for jj = 1:1:length(connection)
        plot3(z(connection(jj,:)),x(connection(jj,:)),y(connection(jj,:)),'Color','b','LineWidth',0.05);
    end
    xlabel('Z(m)'); ylabel('X(m)'); zlabel('Y(m)'); title(sprintf('Timestamp: %d (ms)',timestampList(ii)));
    grid on;
    legend([camera human] ,'camera','human');
    drawnow;
    Frame=getframe(gcf);
    Image=frame2im(Frame);
    [Image,map]=rgb2ind(Image,256);
    if ii == 2
        imwrite(Image,map,'test.gif','gif', 'Loopcount',inf,'DelayTime',0.03);
    else
        imwrite(Image,map,'test.gif','gif','WriteMode','append','DelayTime',0.03);
    end
end