using Distributions
using Plots

function main()
  quantity = 32
  noise = rand(Uniform(-1, 1), quantity)
  plot([1:quantity], noise, ylim=[-2,2])

  savefig("noise.png")
  gui()
  readline()
end

main()