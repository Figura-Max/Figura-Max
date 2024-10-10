function [xout tout] = EulerImplicit(f, t0, x0, T, h)

    # How many steps will be taken?
    n = floor((T - t0)/h);

    # Define the output vectors for t and x
    tout = t0:h:(t0 + n*h);
    xout = zeros(length(x0), n+1);

    # Assign the initial condition x0 into the output vector xout
    xout(:, 1) = x0;

    # Working variables
    t = t0;
    x = x0;

    # Implicit Euler's method until we reach T
    for i = 1:n
        x = EulerImplicit_step(f, t, x, h);
        xout(:, i+1) = x;
        t = tout(i+1);
    end

    # Add one more step just in case T wasn't reached
    if (t != T)
        h = T - t;
        x = EulerImplicit_step(f, t, x, h);
        tout = [tout T];
        xout = [xout x];
    end

    if (nargout == 0)
        plot(tout, xout)
    end

endfunction


function xnew = EulerImplicit_step(f, t, x, h)
    xnew = fsolve(@(z) z - x - h*f(t+h, z), x);
endfunction
