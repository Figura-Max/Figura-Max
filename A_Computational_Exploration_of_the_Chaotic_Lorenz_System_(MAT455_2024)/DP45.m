function [xout tout flag] = DP45(f, t0, x0, T, tolmin, tolmax, hmin, hmax)
    # flag = 0: Success, all tolerances reached
    # flag > 0: Failure, at least one tolerance not reached (number of bad steps)

    if (tolmin >= tolmax || tolmin < 0)
        disp('Choose 0 < tolmin < tolmax. Exiting...');
        return;
    end

    if (hmin >= hmax || hmin < 0)
        disp('Choose 0 < hmin < hmax. Exiting...');
        return;
    end

    if (T <= t0)
        disp('Choose T > t0. Exiting...');
        return;
    end

    flag = 0; # Start assuming success

    tout = [t0];
    xout = [x0];

    t = t0;
    x = x0;
    force_small_h = 1;
    h = hmax; # Start with the largest possible stepsize

    while (t < T)
        if (t + h > T)
            h = T - t;
            force_small_h = 0;
        end

        if (h < hmin && force_small_h == 1)
            h = hmin;
        elseif (h > hmax)
            h = hmax;
        end

        told = t;
        xold = x;

        [x t errest] = DP45_step(f, t, x, h);

        if (errest <= tolmax)
            tout = [tout t];
            xout = [xout x];
            if (errest < tolmin)
                h = 2*h;
            end
        else
            if (h > hmin)
                h = h/2;
                t = told;
                x = xold;
            else
                flag = flag + 1;   # Can't reach this tolerance
                tout = [tout t];
                xout = [xout x];
            end
        end
    end

    if (nargout == 0)
        plot(tout, xout)
    end
endfunction


function [xnew tnew errest] = DP45_step(f, t, x, h)
    k1 = f(t         , x);
    k2 = f(t +  1/5*h, x + h*k1/5);
    k3 = f(t + 3/10*h, x + h*(3*k1 + 9*k2)/40);
    k4 = f(t +  4/5*h, x + h*(44*k1 - 168*k2 + 160*k3)/45);
    k5 = f(t +  8/9*h, x + h*(19372*k1 - 76080*k2 + 64448*k3 - 1908*k4)/6561);
    k6 = f(t +      h, x + h*(477901*k1 - 1806240*k2 + 1495424*k3 + 46746*k4 - 45927*k5)/167904);

    tnew = t + h;

    # Using the 5th-order method
    xnew = x + h*(12985*k1 + 64000*k3 + 92750*k4 - 45927*k5 + 18656*k6)/142464;

    k7 = f(t + h, xnew);

    # Using the 4th-order method
    #xnew = x + h*(1921409*k1 + 9690880*k3 + 13122270*k4 - 5802111*k5 + 1902912*k6 + 534240*k7)/21369600;

    # Error estimate
    errest = h*norm((26341*k1 - 90880*k3 + 790230*k4 - 1086939*k5 + 895488*k6 - 534240*k7)/21369600, "inf");
endfunction
