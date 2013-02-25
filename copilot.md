# A Copilot example

# Introduction
[Copilot](http://leepike.github.com/Copilot/) is a Haskel DSL for defining
software health monitors in embedded systems.

It uses other DSLs called [Atom](https://github.com/tomahawkins/atom) and
[SBV](http://hackage.haskell.org/package/sbv) for generating C code and verification.

# Concepts

The main data type is _Stream_, where _Stream_ is an infinite list.  You need
to specifiy the type of the element so a valid declaration is:

    myFirstStream :: Stream Int

Copilot overloads the ++ operator to lift operands to type _Stream_.

    myStream :: Stream Int
    myStream = [0,1,2] ++ myStream      -- yields [0,1,2] repeating


You can also use _drop_ on Streams.

    drop 1 myStream     -- yields [1,2] ++ [0,1,2] repeating

# Specs

Every Copilot program has a _spec_ defining what condition to monitor and what
to do when that condition occurs.  The action to take when the condition occurs
is called the _trigger_.  The _spec_ from the Copilot paper:  

    propTempRiseShutOff :: Spec
    propTempRiseShutOff = do
      observer "drop 2 temps" (drop 2 temps)
      observer "temps" (temps)
      trigger "over_temp_rise"
        (overTempRise && running) []
      where
    -- continues ...
 
An _observer_ is used for debugging.  When you interpret the _spec_ the value
of the observed value will be printed for each time step.  The form is:

    observer "description" (variable_name)

Where "description" can be an string.  It's just the name of the column in the
interpreter output.

And _trigger_ has the form:

    trigger "functionname" (Stream Bool) [arguments]

The _functionname_ function can be a Haskell function or an external C
function.  The _Stream Bool_ part is the condition to be monitored.  The
_[arguments]_ get passed to _functionname_ when the trigger fires.

Everything after _where_ are the variables used in the _spec_.
Typically the _spec_ defines its own _Streams_ and _extern_ _Streams_.  The purpose
of _extern_ is to model data coming into the monitor from other parts of the
system.  The code generating the _extern_ _Streams_ can be external C functions.

In this example the _Stream_ representing the data input is called _temps_:

    max = 500 -- maximum engine temperature
    temps :: Stream Float
    temps = [max, max, max] ++ temp
    temp = extern "temp" (Just tempin)
    tempin = 100.0:100.0:100.0:repeat 103.0 -- this could be an extern C function

The reason _temps_ has _max_ 3 times at the beginning is just to give it an
initial value.  It'll make sense once you see how the condition _Stream_ is defined.

The _Stream_ that represents the condition to be monitored is called _overTempRise_:

    overTempRise :: Stream Bool
    overTempRise = drop 2 temps > (2.3 + temps)

In the example, we only want the monitor to run when the engine is running,
so another _Stream_ is defined as _running_:

    running :: Stream Bool
    running = extern "running" (Just (repeat True))

Here, _running_ is always _True_ but it could be something more exciting.

The complete program is:

    import Language.Copilot
    import qualified Prelude as P

    propTempRiseShutOff :: Spec
    propTempRiseShutOff = do
      observer "drop 2 temps" (drop 2 temps)
      observer "temps" (temps)
      trigger "over_temp_rise"
        (overTempRise && running) []
      where
      max = 500 -- maximum engine temperature

      temps :: Stream Float
      temps = [max, max, max] ++ temp
      temp = extern "temp" (Just tempin)

      tempin = 100.0:100.0:100.0:repeat 103.0

      overTempRise :: Stream Bool
      overTempRise = drop 2 temps > (2.3 + temps)

      running :: Stream Bool
      running = extern "running" (Just (repeat True))

To interpret (simulate) the _spec_ start ghci, load the module and type:

    interpret 10 propTempRiseShutOff

The output is:

    over_temp_rise:  drop 2 temps:    temps:          
    --               500.0            500.0           
    --               100.0            500.0           
    --               100.0            500.0           
    --               100.0            100.0           
    ()               103.0            100.0           
    ()               103.0            100.0           
    --               103.0            103.0           
    --               103.0            103.0           
    --               103.0            103.0           
    --               103.0            103.0  

The () indicate when the trigger fired.  This occurs when _drop 2 temps_ is
greater than _2.3 + temps_. The "current" temperature value for this tick
is _drop 2 temps_ and the temperature value 2 ticks ago is _temps_.  One
item is dropped from the infinite _Stream_ each tick.
