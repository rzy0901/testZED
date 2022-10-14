clc; clear; close all;
load('data.mat')
keypoints = double(keypoints);
timestampList = double(timestampList);
timestampList = timestampList - timestampList(1);
for ii = 1:1:length(timestampList)
    x = squeeze(keypoints(ii,:,1));
    y = squeeze(keypoints(ii,:,2));
    z = squeeze(keypoints(ii,:,3));
    scatter3(z,x,y,'filled');
    xlabel('Z(m)'); ylabel('X(m)'); zlabel('Y(m)'); title(sprintf('Timestamp: %d (ms)',timestampList(ii)));
    grid on;
    axis equal;
    xlim([-1 0]);
    ylim([-1 1]);
    zlim([-1 1]);
    drawnow;
    Frame=getframe(gcf);
    Image=frame2im(Frame);
    [Image,map]=rgb2ind(Image,256);
    if ii == 1
        imwrite(Image,map,'test.gif','gif', 'Loopcount',inf,'DelayTime',0.03);
    else
        imwrite(Image,map,'test.gif','gif','WriteMode','append','DelayTime',0.03);
    end
end