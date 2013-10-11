function [err, Yhat] = sinusoid_error(T, Y, freq)
    S = sin(2 * pi * freq * T);
    C = cos(2 * pi * freq * T);

    b = [S C] \ Y;
    Yhat = [S C] * b;
    err = sqrt(sum((Y - Yhat) .^ 2));
    
