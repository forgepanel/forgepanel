<?php
declare(strict_types=1);
namespace ForgePanel\Command;
use ForgePanel\Setup\SetupService;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
#[AsCommand(name:'forgepanel:setup:status')]
final class StatusCommand extends Command {
    public function __construct(private SetupService $setup) { parent::__construct(); }
    protected function execute(InputInterface $input,OutputInterface $output):int {
        LocalConsoleGuard::enforce(false);
        $value=$this->setup->status();
        $output->write(json_encode($value,JSON_PRETTY_PRINT|JSON_THROW_ON_ERROR).PHP_EOL,false,OutputInterface::OUTPUT_RAW);
        return Command::SUCCESS;
    }
}
