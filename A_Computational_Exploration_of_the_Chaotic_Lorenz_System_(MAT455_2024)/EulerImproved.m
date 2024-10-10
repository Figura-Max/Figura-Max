function [xout tout] = EulerImproved(f, t0, x0, T, h)
    n = floor((T - t0)/h);
    tout = t0:h:(t0 + n*h);
    xout = zeros(length(x0), n+1);
    
    xout(:, 1) = x0;
    
    t = t0;
    x = x0;
    for i = 1:n
        x = Euler_improved_step(f, t, x, h);
        xout(:, i+1) = x;
        t = tout(i+1);
    end
    if (t < T)
        h = T - t;
        x = Euler_improved_step(f, t, x, h);
        tout = [tout T];
        xout = [xout x];
    end
    
    if (nargout == 0)
        plot(tout, xout, "b")
    end
endfunction

function xnew = Euler_improved_step(f, t, x, h)
    k1 = f(t, x);
    k2 = f(t+h, x + h*k1);
    xnew = x + h*(k1+k2)/2;
    #xnew = x + h*(f(t, x)+f(t+h,x+h*f(t, x)))/2;
endfunction
