periods = [10 12 14 16 18 20];
reps = [01 02 03];

a=1;
for j = 1:length(reps)
    for i = 1:length(periods)
        file(a) = {[load(sprintf('sin%drep0%d.txt',periods(i),reps(j)))]};
        a = a + 1;
    end
end

lens = cellfun('length', file);
mlens = min(lens);


a = 1;
for j = 1:length(reps)
    for i = 1:length(periods)
        b = file{1,a};
        
        T(:,a)=b((length(b)-mlens+2000):end,1);
        Y(:,a)=b((length(b)-mlens+2000):end,2);
        a = a + 1; 
    end
end


format long g       
a = 1;
for j = 1:length(reps)
    for i = 1:length(periods)
        options = optimset('display', 'iter');
        [freqhat] = fmincon(@(freq) sinusoid_error(T(:,a), Y(:,a), freq), 1/(periods(i)/10), [], [], [], [], 0.001, 10, [], options);
        [err(a), Yhat(:,a)] = sinusoid_error(T(:,a), Y(:,a), freqhat);
        periodshat(i, j) = (1/freqhat)*1000;
        periodshats{i, j} = sprintf('%.2f', (1/freqhat)*1000);
        figure(i)
        hold on;
        plot(T(:,a), Y(:,a), 'r');
        plot(T(:,a), Yhat(:,a), 'b');
        a = a + 1;
    end
end
%clf; hold on;
%plot(T, Y, 'r');
%plot(T, Yhat, 'b');
