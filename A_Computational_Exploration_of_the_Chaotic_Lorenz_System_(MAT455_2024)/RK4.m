function [xout tout] = RK4(f, t0, x0, T, h)
    n = floor((T - t0)/h);
    tout = t0:h:(t0 + n*h);
    xout = zeros(length(x0), n+1);
    
    xout(:, 1) = x0;
    
    t = t0;
    x = x0;
    for i = 1:n
        x = RK4_step(f, t, x, h);
        xout(:, i+1) = x;
        t = tout(i+1);
    end
    if (t < T)
        h = T - t;
        x = RK4_step(f, t, x, h);
        tout = [tout T];
        xout = [xout x];
    end
    
    if (nargout == 0)
        plot(tout, xout, "b")
    end
endfunction

function xnew = RK4_step(f, t, x, h)
    k1 = f(t, x);
    k2 = f(t+0.5*h, x + 0.5*h*k1);
    k3 = f(t+0.5*h, x + 0.5*h*k2);
    k4 = f(t+h, x + h*k3);
    xnew = x + h*(k1 + 2*k2 + 2*k3 + k4)/6;
endfunction
